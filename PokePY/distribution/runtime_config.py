from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

APP_NAME = "PokePY"
CLIENT_CONFIG_FILENAME = "pokepy_client.json"


def is_frozen_app() -> bool:
    return bool(getattr(sys, "frozen", False))


def bundled_base_dir() -> Path:
    if is_frozen_app():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)).resolve()
    return Path(__file__).resolve().parents[2]


def project_root_dir() -> Path:
    if is_frozen_app():
        return bundled_base_dir()
    return Path(__file__).resolve().parents[2]


def project_base_dir() -> Path:
    if is_frozen_app():
        return bundled_base_dir() / "PokePY"
    return Path(__file__).resolve().parents[1]


def user_data_dir() -> Path:
    if os.name == "nt":
        root = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support"
    else:
        root = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / APP_NAME


def save_dir() -> Path:
    directory = user_data_dir() / "saves" if is_frozen_app() else project_base_dir() / "saves"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _deduplicate_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        normalized = str(path.expanduser().resolve(strict=False)).casefold()
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(path.expanduser())
    return unique


def _candidate_config_paths() -> list[Path]:
    candidates: list[Path] = []
    explicit_path = os.getenv("POKEPY_CLIENT_CONFIG")
    if explicit_path:
        candidates.append(Path(explicit_path))

    if is_frozen_app():
        executable_dir = Path(sys.executable).resolve().parent
        bundle_dir = bundled_base_dir()
        candidates.extend(
            [
                bundle_dir / CLIENT_CONFIG_FILENAME,
                executable_dir / CLIENT_CONFIG_FILENAME,
                Path.cwd() / CLIENT_CONFIG_FILENAME,
            ]
        )
    else:
        root = project_root_dir()
        candidates.extend(
            [
                root / CLIENT_CONFIG_FILENAME,
                root / "packaging" / CLIENT_CONFIG_FILENAME,
                Path.cwd() / CLIENT_CONFIG_FILENAME,
                Path.cwd() / "packaging" / CLIENT_CONFIG_FILENAME,
            ]
        )
    return _deduplicate_paths(candidates)


def load_client_config_with_source() -> tuple[dict[str, Any], Path | None]:
    for path in _candidate_config_paths():
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            return data, path
    return {}, None


def load_client_config() -> dict[str, Any]:
    data, _ = load_client_config_with_source()
    return data


def config_value(key: str, default: str) -> str:
    env_value = os.getenv(f"POKEPY_{key.upper()}")
    if env_value is not None and env_value != "":
        return env_value

    data = load_client_config()
    lower_key = key.lower()
    if lower_key in data:
        value = data[lower_key]
        return default if value is None else str(value)
    if key in data:
        value = data[key]
        return default if value is None else str(value)
    return default


def config_bool(key: str, default: bool) -> bool:
    raw_default = "1" if default else "0"
    raw_value = config_value(key, raw_default).strip().lower()
    return raw_value not in {"0", "false", "no", "off"}


def config_float(key: str, default: float) -> float:
    raw_value = config_value(key, str(default))
    try:
        return float(raw_value)
    except ValueError:
        return default


def config_int(key: str, default: int) -> int:
    raw_value = config_value(key, str(default))
    try:
        return int(raw_value)
    except ValueError:
        return default
