"""Default configuration values for Cerebrus."""

from __future__ import annotations

from pathlib import Path

from cerebrus.config.models import CacheConfig, CerebrusConfig, ProjectPathsConfig, ToolPaths

DEFAULT_CONFIG_PATH = Path("config/cerebrus.yaml")
DEFAULT_TOOL_PATHS = ToolPaths()
DEFAULT_CACHE = CacheConfig()
DEFAULT_PROJECT_PATHS = ProjectPathsConfig()


def build_default_config() -> CerebrusConfig:
    return CerebrusConfig(
        tool_paths=ToolPaths(
            uaft=DEFAULT_TOOL_PATHS.uaft,
            csvtools_root=DEFAULT_TOOL_PATHS.csvtools_root,
            perfreporttool=DEFAULT_TOOL_PATHS.perfreporttool,
        ),
        cache=CacheConfig(
            directory=DEFAULT_CACHE.directory,
            max_entries=DEFAULT_CACHE.max_entries,
        ),
        project_paths=ProjectPathsConfig(
            definition_file=DEFAULT_PROJECT_PATHS.definition_file,
            cache_file=DEFAULT_PROJECT_PATHS.cache_file,
        ),
    )
