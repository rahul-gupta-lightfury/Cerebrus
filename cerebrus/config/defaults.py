"""Default configuration values for Cerebrus."""

from __future__ import annotations

from pathlib import Path

from cerebrus.config.models import (
    CacheConfig,
    CerebrusConfig,
    ProjectProfile,
    ToolPaths,
)

DEFAULT_CONFIG_PATH = Path("config/cerebrus.yaml")
DEFAULT_PROFILE = ProjectProfile(
    name="default",
    report_type="summary",
    csv_filters=["stat=Unit", "stat=FrameTime"],
    description="Basic summary profile for quick validation runs.",
)
DEFAULT_TOOL_PATHS = ToolPaths()
DEFAULT_CACHE = CacheConfig()


def build_default_config() -> CerebrusConfig:
    return CerebrusConfig(
        tool_paths=ToolPaths(
            uaft=DEFAULT_TOOL_PATHS.uaft,
            csvtools_root=DEFAULT_TOOL_PATHS.csvtools_root,
            perfreporttool=DEFAULT_TOOL_PATHS.perfreporttool,
        ),
        profiles=[
            ProjectProfile(
                name=DEFAULT_PROFILE.name,
                report_type=DEFAULT_PROFILE.report_type,
                csv_filters=list(DEFAULT_PROFILE.csv_filters),
                description=DEFAULT_PROFILE.description,
            )
        ],
        cache=CacheConfig(
            directory=DEFAULT_CACHE.directory,
            max_entries=DEFAULT_CACHE.max_entries,
        ),
    )
