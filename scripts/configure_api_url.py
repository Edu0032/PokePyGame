from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_CONFIG_PATH = PROJECT_ROOT / "pokepy_client.json"
PACKAGING_CONFIG_PATH = PROJECT_ROOT / "packaging" / "pokepy_client.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure the hosted PokePY API URL for source and executable builds.")
    parser.add_argument("https://pokepygame.onrender.com", required=True, help="Hosted API URL, for example https://pokepy-api.onrender.com")
    parser.add_argument("--fallback", action="store_true", default=True, help="Keep local JSON fallback enabled")
    return parser.parse_args()


def build_config(api_url: str, fallback: bool) -> dict[str, object]:
    return {
        "backend_mode": "api",
        "leaderboard_backend": "api",
        "progress_backend": "api",
        "multiplayer_backend": "api",
        "api_base_url": api_url.rstrip("/"),
        "api_timeout_seconds": 8,
        "api_json_fallback": fallback,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    config = build_config(args.api_url, args.fallback)
    write_json(CLIENT_CONFIG_PATH, config)
    write_json(PACKAGING_CONFIG_PATH, config)
    print(f"Client configuration written to {CLIENT_CONFIG_PATH}")
    print(f"Packaging configuration written to {PACKAGING_CONFIG_PATH}")


if __name__ == "__main__":
    main()
