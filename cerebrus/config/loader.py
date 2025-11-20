"""Configuration loader utilities."""

from __future__ import annotations

import importlib
import importlib.util
import json
import logging
from pathlib import Path
from typing import Any

_yaml_module = importlib.util.find_spec("yaml")
if _yaml_module is not None:  # pragma: no cover - environment dependent
    yaml = importlib.import_module("yaml")  # type: ignore[assignment]
else:

    class _YamlShim:
        @staticmethod
        def safe_load(stream: str | Any) -> Any:
            if isinstance(stream, str):
                return json.loads(stream)
            return json.load(stream)

    yaml = _YamlShim()  # type: ignore[assignment]

from cerebrus.config import defaults
from cerebrus.config.models import (
    CacheConfig,
    CerebrusConfig,
    ProjectPathsConfig,
    ProjectProfile,
    ToolPaths,
)
from cerebrus.config.schema import SchemaError, validate


LOGGER = logging.getLogger(__name__)


def _coerce_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    return Path(value).expanduser()


def load_config_from_file(path: Path) -> CerebrusConfig:
    if not path.exists():
        return defaults.build_default_config()

    with path.open("r", encoding="utf-8") as handle:
        try:
            if path.suffix.lower() == ".json":
                data = json.load(handle)
            else:
                data = yaml.safe_load(handle) or {}
        except Exception as exc:  # pragma: no cover - defensive fallback
            LOGGER.warning(
                "Failed to parse configuration %s (%s); falling back to defaults",
                path,
                exc,
            )
            return defaults.build_default_config()

    validate(data)

    tool_paths_raw = data["tool_paths"]
    tool_paths = ToolPaths(
        uaft=_coerce_path(tool_paths_raw.get("uaft")),
        csvtools_root=_coerce_path(tool_paths_raw.get("csvtools_root")),
        perfreporttool=_coerce_path(tool_paths_raw.get("perfreporttool")),
    )

    cache_data = data.get("cache", {})
    cache_directory = (
        _coerce_path(cache_data.get("directory")) or defaults.DEFAULT_CACHE.directory
    )
    cache = CacheConfig(
        directory=cache_directory,
        max_entries=cache_data.get("max_entries", defaults.DEFAULT_CACHE.max_entries),
    )

    project_paths_data = data.get("project_paths", {})
    project_paths = ProjectPathsConfig(
        definition_file=(
            _coerce_path(project_paths_data.get("definition_file"))
            or defaults.DEFAULT_PROJECT_PATHS.definition_file
        ),
        cache_file=_coerce_path(project_paths_data.get("cache_file"))
        or defaults.DEFAULT_PROJECT_PATHS.cache_file,
    )

    profiles = _parse_profiles(data["profiles"])

    return CerebrusConfig(
        tool_paths=tool_paths,
        profiles=profiles,
        cache=cache,
        project_paths=project_paths,
    )


__all__ = ["load_config_from_file", "SchemaError"]
