"""Configuration loading helpers."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

from cerebrus.config import defaults
from cerebrus.config.models import AppConfig


def load_config_from_file(path: Path) -> AppConfig:
    """Load application configuration from ``path`` or return defaults when missing.

    The loader accepts JSON or YAML-formatted content. The return value is always
    an :class:`~cerebrus.config.models.AppConfig` instance with at least one
    profile configured.
    """

    if not path.exists():
        return defaults.DEFAULT_CONFIG

    data = _parse_file(path)
    if not isinstance(data, Mapping):
        return defaults.DEFAULT_CONFIG

    return AppConfig.from_mapping(data)


_yaml_spec = importlib.util.find_spec("yaml")
if _yaml_spec:
    import yaml  # type: ignore
else:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore


def _parse_file(path: Path) -> Any:
    content = path.read_text()
    if yaml is not None:
        return yaml.safe_load(content)
    return json.loads(content)
