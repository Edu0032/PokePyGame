from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib import error, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_CONFIG_PATH = PROJECT_ROOT / "pokepy_client.json"


def load_api_url() -> str:
    if not CLIENT_CONFIG_PATH.exists():
        return "https://pokepygame.onrender.com"
    data = json.loads(CLIENT_CONFIG_PATH.read_text(encoding="utf-8"))
    return str(data.get("api_base_url") or "https://pokepygame.onrender.com").rstrip("/")


def http_json(method: str, url: str, payload: dict | None = None, timeout: float = 65) -> object:
    body = None
    headers = {}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8")
            return json.loads(content) if content else {}
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} -> HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"{method} {url} -> {exc.reason}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the hosted PokePY API used by the game client.")
    parser.add_argument("--api-url", default=load_api_url())
    parser.add_argument("--write-test-score", action="store_true")
    args = parser.parse_args()
    base_url = args.api_url.rstrip("/")

    print(f"API base URL: {base_url}")
    for path in ["/health", "/health/ready", "/leaderboard", "/multiplayer/capabilities"]:
        url = f"{base_url}{path}"
        started = time.perf_counter()
        result = http_json("GET", url)
        elapsed = time.perf_counter() - started
        print(f"OK {path} ({elapsed:.2f}s): {result}")

    if args.write_test_score:
        payload = {"player_name": "HealthCheck", "elapsed_seconds": 9999}
        result = http_json("POST", f"{base_url}/leaderboard", payload)
        print(f"OK POST /leaderboard: {result}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
