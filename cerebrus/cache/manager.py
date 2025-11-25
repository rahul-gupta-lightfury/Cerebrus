"""Simple cache directory management."""

from __future__ import annotations

import shutil
from pathlib import Path

from cerebrus.config.models import CacheConfig
from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


class CacheManager:
    """Manage creation and cleanup of the Cerebrus cache directory."""

    def __init__(self, config: CacheConfig):
        self.config = config

    @property
    def directory(self) -> Path:
        """Return the configured cache directory path."""

        return self.config.directory

    def ensure_cache(self) -> Path:
        """Create the cache directory if needed and enforce retention."""

        path = self.directory
        path.mkdir(parents=True, exist_ok=True)
        self._enforce_max_entries(path)
        LOGGER.info("Cache directory ready at %s", path)
        return path

    def _enforce_max_entries(self, directory: Path) -> None:
        """Trim cache entries to respect the configured limit."""

        if self.config.max_entries <= 0:
            return

        entries = sorted(directory.iterdir(), key=lambda item: item.stat().st_mtime)
        excess = len(entries) - self.config.max_entries
        if excess <= 0:
            return

        for path in entries[:excess]:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                LOGGER.info("Evicted cache entry %s", path)
            except OSError as exc:
                LOGGER.warning("Failed to evict cache entry %s: %s", path, exc)
