#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
steam="${STEAM_COMPAT_CLIENT_INSTALL_PATH:-$HOME/.local/share/Steam}"
proton="$steam/steamapps/common/Proton 11.0/proton"
test -s "$root/game/SEGA Rally_SSE1.exe"
mkdir -p "$root/compatdata" "$root/logs"
export STEAM_COMPAT_CLIENT_INSTALL_PATH="$steam" STEAM_COMPAT_DATA_PATH="$root/compatdata"
"$proton" run cmd.exe /c ver
prefix="$root/compatdata/pfx"
saved="$prefix/drive_c/users/steamuser/Documents/SEGA Rally/Saved Games"
shared="$prefix/drive_c/users/Public/Documents/SEGA Rally/Shared Data"
mkdir -p "$saved" "$shared/Ghosts" "$shared/Rank Table"
if [[ ! -f "$saved/config.ini" ]]; then
    cp "$root/config.ini" "$saved/config.ini"
fi
python3 - "$root" <<'PY'
import sys
from pathlib import Path
root = Path(sys.argv[1])
install = "Z:" + str(root / "game").replace("/", "\\\\")
reg = ('Windows Registry Editor Version 5.00\r\n\r\n'
       '[HKEY_LOCAL_MACHINE\\Software\\Wow6432Node\\SEGA\\SEGA Rally]\r\n'
       f'"installdir"="{install}"\r\n"sku"="Europe"\r\n"language"="English"\r\n')
(root / "logs/install.reg").write_bytes(reg.encode("utf-16"))
PY
reg="$root/logs/install.reg"
"$proton" run regedit /S "Z:${reg//\//\\}"
