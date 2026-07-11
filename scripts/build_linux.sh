#!/usr/bin/env bash
set -euo pipefail
API_URL="${1:-https://pokepygame.onrender.com}"
python scripts/build_executable.py --api-url "$API_URL" --onedir
