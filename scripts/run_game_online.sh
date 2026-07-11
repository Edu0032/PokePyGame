#!/usr/bin/env bash
set -euo pipefail
export POKEPY_API_BASE_URL="${1:-https://pokepygame.onrender.com}"
export POKEPY_BACKEND_MODE=api
export POKEPY_LEADERBOARD_BACKEND=api
export POKEPY_PROGRESS_BACKEND=api
export POKEPY_MULTIPLAYER_BACKEND=api
python -m PokePY.main
