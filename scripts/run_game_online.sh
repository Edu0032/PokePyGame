#!/usr/bin/env bash
set -euo pipefail
API_URL="${1:-http://127.0.0.1:8000}"
export POKEPY_BACKEND_MODE=api
export POKEPY_LEADERBOARD_BACKEND=api
export POKEPY_PROGRESS_BACKEND=api
export POKEPY_API_BASE_URL="$API_URL"
python -m PokePY.main
