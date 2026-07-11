from argparse import Namespace
from pathlib import Path

import pytest
from scripts import build_executable


def args(**overrides):
    values = {
        "api_url": build_executable.DEFAULT_API_URL,
        "timeout": 65.0,
        "fallback": False,
        "name": "PokePY",
        "onedir": True,
        "onefile": False,
        "console": False,
        "allow_local_api": False,
        "skip_zip": False,
    }
    values.update(overrides)
    return Namespace(**values)


def test_public_build_rejects_localhost():
    with pytest.raises(ValueError):
        build_executable.validate_api_url("http://127.0.0.1:8000", False)


def test_public_build_accepts_render_url():
    assert (
        build_executable.validate_api_url(
            "https://pokepygame.onrender.com/",
            False,
        )
        == build_executable.DEFAULT_API_URL
    )


def test_packaged_config_targets_bundle_root():
    build_executable.write_runtime_config(
        build_executable.runtime_config(
            build_executable.DEFAULT_API_URL,
            65.0,
            False,
        )
    )
    command = build_executable.build_command(args())
    joined = " ".join(command)
    config_argument = build_executable.add_data_arg(
        build_executable.CLIENT_CONFIG_FILE,
        ".",
    )
    assert config_argument in command
    assert "127.0.0.1" not in joined


def test_release_zip_contains_distribution(tmp_path: Path, monkeypatch):
    distribution = tmp_path / "PokePY"
    distribution.mkdir()
    (distribution / "PokePY.exe").write_bytes(b"test")
    monkeypatch.setattr(
        build_executable,
        "RELEASE_DIR",
        tmp_path / "release",
    )
    build_executable.RELEASE_DIR.mkdir()
    zip_path, checksum = build_executable.create_release_zip(
        distribution,
        "PokePY",
    )
    assert zip_path.is_file()
    assert checksum.is_file()
