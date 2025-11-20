from __future__ import annotations

from pathlib import Path

from cerebrus.config import defaults
from cerebrus.config.loader import load_config_from_file


def test_load_config_from_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yaml"
    config = load_config_from_file(missing)
    assert config.cache.directory == defaults.DEFAULT_CACHE.directory
    assert config.project_paths.definition_file == defaults.DEFAULT_PROJECT_PATHS.definition_file
