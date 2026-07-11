import json
from pathlib import Path

from scripts.validate_release import (
    EXPECTED_API_URL,
    validate_client_config,
    validate_distribution,
)


def config_payload():
    return {
        "backend_mode": "api",
        "leaderboard_backend": "api",
        "progress_backend": "api",
        "multiplayer_backend": "api",
        "api_base_url": EXPECTED_API_URL,
        "api_timeout_seconds": 65,
        "api_json_fallback": False,
    }


def test_valid_client_config_has_no_errors(tmp_path: Path):
    path = tmp_path / "pokepy_client.json"
    path.write_text(json.dumps(config_payload()), encoding="utf-8")
    assert validate_client_config(path) == []


def test_distribution_validation_detects_embedded_configuration(
    tmp_path: Path,
):
    distribution = tmp_path / "PokePY"
    distribution.mkdir()
    (distribution / "PokePY.exe").write_bytes(b"binary")
    (distribution / "pokepy_client.json").write_text(
        json.dumps(config_payload()),
        encoding="utf-8",
    )
    (distribution / "BUILD_INFO.json").write_text(
        json.dumps({"api_base_url": EXPECTED_API_URL}),
        encoding="utf-8",
    )
    assert validate_distribution(distribution) == []
