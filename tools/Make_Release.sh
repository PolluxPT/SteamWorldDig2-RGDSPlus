#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python3 "$BASE/tools/audit_public.py"
python3 "$BASE/tools/package_release.py"
