"""Set the opponent AI level in the European PC release using the user's own data."""
import argparse
import hashlib
import os
from pathlib import Path
import struct
import tempfile
import zlib


# SHA-256 of the unpacked tables, before and after changing only the AI fields.
TABLES = [
    ("System/GameMode_data.sbf", 204,
     "77593a976781b1c3d203758be680c548493c80b30fc244cd6fd8ad2277bb96fa",
     "1ca074ea80898932472b418653b6205d8ec3c00e027c250c00d9c343a498b5f9"),
    ("Main_release/system/pack_data.sbf", 144,
     "e8ed2cc2ea774ed1d0c395052738aa30f5ce26ce2161b1818cf6d8a40d3cd672",
     "227193009ddb3bfdc3362b5025daa1a0fa6337dbd437fa26517f2c9b2f83643f"),
]


def unpack(raw):
    if raw[:4] != b"SBZ1":
        raise ValueError("Formato de tabela desconhecido")
    data = bytearray(zlib.decompress(raw[8:]))
    if len(data) != struct.unpack_from("<I", raw, 4)[0]:
        raise ValueError("Tamanho de tabela incorreto")
    return data


def ai_offsets(data):
    def uint(offset):
        return struct.unpack_from("<I", data, offset)[0]

    for record in range(uint(20)):
        header = uint(28 + 8 * record)
        external_refs = header + 20 + 4 * uint(header + 16)
        base = external_refs + 4 + 4 * uint(external_refs)
        names = base + uint(header + 8)
        for field in range(uint(names + 4)):
            name, value = struct.unpack_from("<II", data, names + 8 + 8 * field)
            start = base + name
            key = data[start:data.index(0, start)].split(b".")[-1].lower()
            if key in (b"road_ai_level", b"off_road_ai_level"):
                yield base + value


def atomic_write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        name = Path(temp.name)
        try:
            temp.write(raw)
            temp.flush()
            os.fsync(temp.fileno())
        except BaseException:
            temp.close()
            name.unlink(missing_ok=True)
            raise
    try:
        os.replace(name, path)
    finally:
        name.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("facil", "original"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    updates = []
    for relative, expected_count, stock, easy in TABLES:
        path = args.root / "game" / relative
        backup = args.root / "backups" / "tabelas-originais" / relative
        raw = path.read_bytes()
        data = unpack(raw)
        digest = hashlib.sha256(data).hexdigest()
        if digest not in (stock, easy):
            raise ValueError(f"Arquivo de outra versão ou já modificado: {path}")
        if backup.exists() and hashlib.sha256(unpack(backup.read_bytes())).hexdigest() != stock:
            raise ValueError(f"Backup incompatível: {backup}")
        if digest == easy and not backup.exists():
            raise ValueError(f"Falta o backup original: {backup}")
        if args.mode == "original":
            if digest == easy:
                updates.append((path, backup.read_bytes()))
        elif digest == stock:
            offsets = list(ai_offsets(data))
            if len(set(offsets)) != expected_count:
                raise ValueError(f"Número de parâmetros inesperado: {path}")
            for offset in offsets:
                struct.pack_into("<f", data, offset, 0.0)
            if hashlib.sha256(data).hexdigest() != easy:
                raise ValueError(f"Falha de verificação: {path}")
            if not backup.exists():
                updates.append((backup, raw))
            updates.append((path, raw[:8] + zlib.compress(data)))
    for path, raw in updates:
        atomic_write(path, raw)
    print(f"Dificuldade aplicada: {args.mode}")


if __name__ == "__main__":
    main()
