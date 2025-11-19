"""Cache management helpers."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from cerebrus.config.models import CacheConfig
from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class CacheManager:
    """Ensure cache directories exist and enforce simple retention policies."""

    config: CacheConfig

    def ensure_cache(self) -> Path:
        """Create the cache directory if needed and apply retention rules."""
        directory = self.config.directory
        directory.mkdir(parents=True, exist_ok=True)
        LOGGER.debug("Ensured cache directory exists at %s", directory)
        self._enforce_limit(directory)
        return directory

    def _enforce_limit(self, directory: Path) -> None:
        """Trim cache entries when exceeding the configured limit."""
        max_entries = self.config.max_entries
        if max_entries <= 0:
            return

        entries: list[Path] = [path for path in directory.iterdir() if path.exists()]
        if len(entries) <= max_entries:
            return

        entries.sort(key=self._mtime)
        while len(entries) > max_entries:
            stale = entries.pop(0)
            self._remove_path(stale)

    @staticmethod
    def _mtime(path: Path) -> float:
        try:
            return path.stat().st_mtime
        except OSError:
            return 0.0

    @staticmethod
    def _remove_path(path: Path) -> None:
        LOGGER.info("Removing stale cache entry: %s", path)
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
