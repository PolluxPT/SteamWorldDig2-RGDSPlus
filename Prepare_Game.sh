#!/bin/sh
# Run on a Linux PC, not from the console's Applications menu.
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command -v python3 >/dev/null 2>&1 || { echo 'Python 3.10 or newer is required on the preparation PC.' >&2; exit 1; }
exec python3 "$BASE/tools/prepare_game.py" "$@"
