#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
steam="${STEAM_COMPAT_CLIENT_INSTALL_PATH:-$HOME/.local/share/Steam}"
proton="$steam/steamapps/common/Proton 11.0/proton"
export STEAM_COMPAT_CLIENT_INSTALL_PATH="$steam" STEAM_COMPAT_DATA_PATH="$root/compatdata"
export DXVK_FRAME_RATE=60 DXVK_LOG_PATH="$root/logs"
unset LD_PRELOAD
mkdir -p "$root/compatdata" "$root/logs"
cd "$root/game"
exec "$proton" waitforexitandrun "$PWD/SEGA Rally_SSE1.exe" >"$root/logs/jogo.log" 2>&1
