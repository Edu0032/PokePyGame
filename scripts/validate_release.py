from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_API_URL = "https://pokepygame.onrender.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a PokePY source tree or packaged distribution.")
    parser.add_argument("--distribution", type=Path)
    return parser.parse_args()


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Configuração inválida: {path}")
    return data


def validate_client_config(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"Configuração ausente: {path}"]
    try:
        config = load_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [f"Configuração inválida em {path}: {error}"]
    api_url = str(config.get("api_base_url", "")).rstrip("/")
    parsed = urlparse(api_url)
    if api_url != EXPECTED_API_URL:
        errors.append(f"URL inesperada em {path}: {api_url}")
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"URL pública inválida em {path}: {api_url}")
    if float(config.get("api_timeout_seconds", 0)) < 60:
        errors.append(f"Timeout curto para Render Free em {path}")
    if config.get("api_json_fallback") is not False:
        errors.append(f"Fallback online deve permanecer desativado em {path}")
    for key in (
        "backend_mode",
        "leaderboard_backend",
        "progress_backend",
        "multiplayer_backend",
    ):
        if config.get(key) != "api":
            errors.append(f"{key} deve ser 'api' em {path}")
    return errors


def validate_source_tree(root: Path = PROJECT_ROOT) -> list[str]:
    errors: list[str] = []
    required = [
        root / "PokePY" / "main.py",
        root / "PokePY" / "api" / "main.py",
        root / "render.yaml",
        root / "requirements-api.txt",
        root / "requirements-build.txt",
        root / "scripts" / "build_executable.py",
        root / "pokepy_client.json",
        root / "packaging" / "pokepy_client.json",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Arquivo obrigatório ausente: {path.relative_to(root)}")
    errors.extend(validate_client_config(root / "pokepy_client.json"))
    errors.extend(validate_client_config(root / "packaging" / "pokepy_client.json"))
    return errors


def find_packaged_config(distribution: Path) -> Path | None:
    candidates = [
        distribution / "pokepy_client.json",
        distribution / "_internal" / "pokepy_client.json",
    ]
    return next((path for path in candidates if path.is_file()), None)


def validate_distribution(distribution: Path) -> list[str]:
    errors: list[str] = []
    if not distribution.exists():
        return [f"Distribuição não encontrada: {distribution}"]
    if distribution.is_dir():
        executable_names = {"PokePY", "PokePY.exe"}
        if not any((distribution / name).is_file() for name in executable_names):
            errors.append("Executável PokePY não encontrado na distribuição.")
        config_path = find_packaged_config(distribution)
        if config_path is None:
            errors.append("pokepy_client.json não foi incorporado à distribuição.")
        else:
            errors.extend(validate_client_config(config_path))
        build_info = distribution / "BUILD_INFO.json"
        if not build_info.is_file():
            errors.append("BUILD_INFO.json não encontrado na distribuição.")
        else:
            data = load_json(build_info)
            if data.get("api_base_url") != EXPECTED_API_URL:
                errors.append("BUILD_INFO.json contém URL de API incorreta.")
    return errors


def main() -> None:
    args = parse_args()
    errors = validate_source_tree()
    if args.distribution:
        errors.extend(validate_distribution(args.distribution.resolve()))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("PokePY release validation passed.")


if __name__ == "__main__":
    main()
