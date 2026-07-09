#!/usr/bin/env bash
set -euo pipefail
export POKEPY_BACKEND_MODE=json
export POKEPY_LEADERBOARD_BACKEND=json
export POKEPY_PROGRESS_BACKEND=json
python -m PokePY.main
