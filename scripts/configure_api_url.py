from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_CONFIG_PATH = PROJECT_ROOT / "pokepy_client.json"
PACKAGING_CONFIG_PATH = PROJECT_ROOT / "packaging" / "pokepy_client.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure the hosted PokePY API URL for source and executable builds."
    )
    parser.add_argument(
        "--api-url",
        required=True,
        help="Hosted API URL, for example https://pokepygame.onrender.com",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="HTTP timeout used by the game client.",
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable local JSON fallback when the online API is temporarily unavailable.",
    )
    return parser.parse_args()


def build_config(api_url: str, timeout: float, fallback: bool) -> dict[str, object]:
    return {
        "backend_mode": "api",
        "leaderboard_backend": "api",
        "progress_backend": "api",
        "multiplayer_backend": "api",
        "api_base_url": api_url.rstrip("/"),
        "api_timeout_seconds": timeout,
        "api_json_fallback": fallback,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    config = build_config(
        api_url=args.api_url,
        timeout=args.timeout,
        fallback=not args.no_fallback,
    )

    write_json(CLIENT_CONFIG_PATH, config)
    write_json(PACKAGING_CONFIG_PATH, config)

    print(f"Client configuration written to {CLIENT_CONFIG_PATH}")
    print(f"Packaging configuration written to {PACKAGING_CONFIG_PATH}")


if __name__ == "__main__":
    main()
