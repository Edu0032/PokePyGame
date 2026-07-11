import json
from pathlib import Path

from PokePY.distribution import runtime_config


def test_false_boolean_is_preserved(monkeypatch, tmp_path: Path):
    config_path = tmp_path / "client.json"
    config_path.write_text(
        json.dumps({"api_json_fallback": False}),
        encoding="utf-8",
    )
    monkeypatch.setenv("POKEPY_CLIENT_CONFIG", str(config_path))
    assert runtime_config.config_bool("API_JSON_FALLBACK", True) is False


def test_environment_variable_overrides_json(monkeypatch, tmp_path: Path):
    config_path = tmp_path / "client.json"
    config_path.write_text(
        json.dumps({"api_base_url": "https://json.example"}),
        encoding="utf-8",
    )
    monkeypatch.setenv("POKEPY_CLIENT_CONFIG", str(config_path))
    monkeypatch.setenv("POKEPY_API_BASE_URL", "https://env.example")
    assert runtime_config.config_value("API_BASE_URL", "missing") == "https://env.example"


def test_explicit_config_source_is_reported(monkeypatch, tmp_path: Path):
    config_path = tmp_path / "client.json"
    config_path.write_text(
        json.dumps({"backend_mode": "api"}),
        encoding="utf-8",
    )
    monkeypatch.setenv("POKEPY_CLIENT_CONFIG", str(config_path))
    data, source = runtime_config.load_client_config_with_source()
    assert data["backend_mode"] == "api"
    assert source == config_path


def test_candidate_paths_are_deduplicated(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    paths = runtime_config._candidate_config_paths()
    normalized = [str(path.resolve(strict=False)).casefold() for path in paths]
    assert len(normalized) == len(set(normalized))
