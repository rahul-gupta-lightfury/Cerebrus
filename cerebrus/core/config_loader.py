"""Facade for loading Cerebrus configuration."""

from __future__ import annotations

from pathlib import Path

from cerebrus.config.loader import load_config_from_file
from cerebrus.config.models import CerebrusConfig


class ConfigLoader:
    """Load configuration with default search paths."""

    def __init__(self, default_path: Path | None = None) -> None:
        self.default_path = default_path or Path("config/cerebrus.yaml")

    def load(self, path: Path | None = None) -> CerebrusConfig:
        return load_config_from_file(path or self.default_path)
