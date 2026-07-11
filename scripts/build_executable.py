from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
RELEASE_DIR = PROJECT_ROOT / "release"
RUNTIME_DIR = BUILD_DIR / "runtime"
CLIENT_CONFIG_FILE = RUNTIME_DIR / "pokepy_client.json"
DEFAULT_API_URL = "https://pokepygame.onrender.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the PokePY client and embed its hosted API configuration.")
    parser.add_argument(
        "--api-url",
        default=os.getenv("POKEPY_API_BASE_URL", DEFAULT_API_URL),
        help="Public API URL embedded in the executable.",
    )
    parser.add_argument("--timeout", type=float, default=65.0)
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Allow local JSON fallback. Disabled in the official online build.",
    )
    parser.add_argument("--name", default="PokePY")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--onedir", action="store_true", help="Folder distribution.")
    mode.add_argument("--onefile", action="store_true", help="Single-file build.")
    parser.add_argument("--console", action="store_true")
    parser.add_argument(
        "--allow-local-api",
        action="store_true",
        help="Allow localhost API URLs for development-only builds.",
    )
    parser.add_argument(
        "--skip-zip",
        action="store_true",
        help="Skip release ZIP creation.",
    )
    return parser.parse_args()


def data_separator() -> str:
    return ";" if os.name == "nt" else ":"


def add_data_arg(source: Path, target_directory: str) -> str:
    return f"{source}{data_separator()}{target_directory}"


def validate_api_url(api_url: str, allow_local: bool) -> str:
    normalized = api_url.strip().rstrip("/")
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("A URL da API deve ser uma URL HTTP/HTTPS válida.")
    local_hosts = {"127.0.0.1", "localhost", "0.0.0.0"}
    if parsed.hostname in local_hosts and not allow_local:
        raise ValueError("Build público recusado: use a API hospedada ou passe --allow-local-api.")
    return normalized


def runtime_config(api_url: str, timeout: float, fallback: bool) -> dict[str, object]:
    return {
        "backend_mode": "api",
        "leaderboard_backend": "api",
        "progress_backend": "api",
        "multiplayer_backend": "api",
        "api_base_url": api_url,
        "api_timeout_seconds": timeout,
        "api_json_fallback": fallback,
    }


def write_runtime_config(config: dict[str, object]) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    CLIENT_CONFIG_FILE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def clean_previous_outputs(name: str) -> None:
    for path in (
        BUILD_DIR,
        DIST_DIR / name,
        DIST_DIR / f"{name}.exe",
        RELEASE_DIR / f"{name}-Windows.zip",
        RELEASE_DIR / f"{name}-Linux.zip",
        PROJECT_ROOT / f"{name}.spec",
    ):
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)


def build_command(args: argparse.Namespace) -> list[str]:
    mode_flag = "--onefile" if args.onefile else "--onedir"
    window_flag = "--console" if args.console else "--windowed"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        mode_flag,
        window_flag,
        "--name",
        args.name,
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR / "pyinstaller"),
        "--specpath",
        str(BUILD_DIR / "spec"),
    ]
    data_items = [
        (PROJECT_ROOT / "PokePY" / "sprites", "PokePY/sprites"),
        (PROJECT_ROOT / "PokePY" / "backgrounds", "PokePY/backgrounds"),
        (PROJECT_ROOT / "PokePY" / "mapa", "PokePY/mapa"),
        (CLIENT_CONFIG_FILE, "."),
    ]
    for source, target in data_items:
        if not source.exists():
            raise FileNotFoundError(f"Arquivo de build ausente: {source}")
        command.extend(["--add-data", add_data_arg(source, target)])
    command.extend(
        [
            "--hidden-import",
            "pygame",
            "--hidden-import",
            "requests",
            str(PROJECT_ROOT / "PokePY" / "main.py"),
        ]
    )
    return command


def ensure_pyinstaller_available() -> None:
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--version"],
        check=True,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def distribution_path(args: argparse.Namespace) -> Path:
    if args.onefile:
        suffix = ".exe" if os.name == "nt" else ""
        return DIST_DIR / f"{args.name}{suffix}"
    return DIST_DIR / args.name


def finalize_distribution(
    args: argparse.Namespace,
    config: dict[str, object],
) -> Path:
    output = distribution_path(args)
    if not output.exists():
        raise FileNotFoundError(f"Saída do PyInstaller não encontrada: {output}")
    if output.is_dir():
        (output / "pokepy_client.json").write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        manifest_path = output / "BUILD_INFO.json"
    else:
        manifest_path = output.with_suffix(output.suffix + ".build.json")
    manifest_path.write_text(
        json.dumps(
            {
                "application": args.name,
                "distribution_mode": "onefile" if args.onefile else "onedir",
                "api_base_url": config["api_base_url"],
                "api_timeout_seconds": config["api_timeout_seconds"],
                "api_json_fallback": config["api_json_fallback"],
                "python": sys.version.split()[0],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return output


def create_release_zip(output: Path, name: str) -> tuple[Path, Path]:
    platform_name = "Windows" if os.name == "nt" else "Linux"
    zip_path = RELEASE_DIR / f"{name}-{platform_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        if output.is_dir():
            for path in sorted(output.rglob("*")):
                if path.is_file():
                    archive.write(path, Path(name) / path.relative_to(output))
        else:
            archive.write(output, output.name)
            build_info = output.with_suffix(output.suffix + ".build.json")
            if build_info.exists():
                archive.write(build_info, build_info.name)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    checksum_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")
    return zip_path, checksum_path


def main() -> None:
    args = parse_args()
    api_url = validate_api_url(args.api_url, args.allow_local_api)
    config = runtime_config(api_url, args.timeout, args.fallback)
    clean_previous_outputs(args.name)
    write_runtime_config(config)
    ensure_pyinstaller_available()
    subprocess.run(build_command(args), cwd=PROJECT_ROOT, check=True)
    output = finalize_distribution(args, config)
    print(f"Distribuição criada em: {output}")
    print(f"API incorporada: {api_url}")
    if not args.skip_zip:
        zip_path, checksum_path = create_release_zip(output, args.name)
        print(f"ZIP para GitHub Release: {zip_path}")
        print(f"SHA-256: {checksum_path}")


if __name__ == "__main__":
    main()
