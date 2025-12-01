"""Default configuration values for Cerebrus."""

from __future__ import annotations

from pathlib import Path

from cerebrus.config.models import AppConfig, CacheConfig, ProfileConfig

DEFAULT_CACHE = CacheConfig(directory=Path(".cerebrus-cache"), max_entries=50)
DEFAULT_PROFILE = ProfileConfig(
    name="default", report_type="summary", nickname="Default Profile"
)
DEFAULT_CONFIG = AppConfig(
    version=1, tool_paths={}, profiles=[DEFAULT_PROFILE], cache=DEFAULT_CACHE
)
