#!/usr/bin/env bash
set -euo pipefail
API_URL="${1:-http://127.0.0.1:8000}"
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-build.txt
python scripts/build_executable.py --api-url "$API_URL"
