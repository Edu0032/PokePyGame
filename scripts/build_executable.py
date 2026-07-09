from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = PROJECT_ROOT / "build" / "runtime"
CLIENT_CONFIG_FILE = RUNTIME_DIR / "pokepy_client.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a distributable PokePY executable with PyInstaller.")
    parser.add_argument("--api-url", default=os.getenv("POKEPY_API_BASE_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--name", default="PokePY")
    parser.add_argument("--windowed", action="store_true", default=True)
    parser.add_argument("--console", action="store_true")
    parser.add_argument("--onedir", action="store_true", help="Build a folder distribution instead of a single executable.")
    parser.add_argument("--clean", action="store_true", default=True)
    return parser.parse_args()


def data_separator() -> str:
    return ";" if os.name == "nt" else ":"


def add_data_arg(source: Path, target: str) -> str:
    return f"{source}{data_separator()}{target}"


def write_runtime_config(api_url: str) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    CLIENT_CONFIG_FILE.write_text(
        json.dumps(
            {
                "backend_mode": "api",
                "leaderboard_backend": "api",
                "progress_backend": "api",
                "multiplayer_backend": "api",
                "api_base_url": api_url.rstrip("/"),
                "api_timeout_seconds": 8,
                "api_json_fallback": True,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def build_command(args: argparse.Namespace) -> list[str]:
    mode_flag = "--onedir" if args.onedir else "--onefile"
    window_flag = "--console" if args.console else "--windowed"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        mode_flag,
        window_flag,
        "--name",
        args.name,
    ]
    if args.clean:
        command.append("--clean")
    data_items = [
        (PROJECT_ROOT / "PokePY" / "sprites", "PokePY/sprites"),
        (PROJECT_ROOT / "PokePY" / "backgrounds", "PokePY/backgrounds"),
        (PROJECT_ROOT / "PokePY" / "mapa", "PokePY/mapa"),
        (CLIENT_CONFIG_FILE, "pokepy_client.json"),
    ]
    for source, target in data_items:
        command.extend(["--add-data", add_data_arg(source, target)])
    command.extend(["--hidden-import", "pygame", "--hidden-import", "requests", str(PROJECT_ROOT / "PokePY" / "main.py")])
    return command


def ensure_pyinstaller_available() -> None:
    if shutil.which("pyinstaller") is None:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], check=True, cwd=PROJECT_ROOT)


def main() -> None:
    args = parse_args()
    write_runtime_config(args.api_url)
    ensure_pyinstaller_available()
    subprocess.run(build_command(args), cwd=PROJECT_ROOT, check=True)
    print(f"Executable package created in: {PROJECT_ROOT / 'dist'}")


if __name__ == "__main__":
    main()
