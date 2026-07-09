#!/usr/bin/env bash
set -euo pipefail
pytest --cov=PokePY --cov-report=term-missing
