"""Cache directory management."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from cerebrus.config.models import CacheConfig


class CacheManager:
    """Handle cache directory creation and eviction policy."""

    def __init__(self, config: CacheConfig) -> None:
        self.config = config

    def ensure_cache(self) -> Path:
        """Create the cache directory if needed and enforce retention."""
        cache_dir = self.config.directory
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._enforce_max_entries(cache_dir)
        return cache_dir

    def _enforce_max_entries(self, cache_dir: Path) -> None:
        entries: Iterable[Path] = cache_dir.iterdir()
        sorted_entries = sorted(entries, key=lambda path: path.stat().st_mtime, reverse=True)

        if len(sorted_entries) <= self.config.max_entries:
            return

        for path in sorted_entries[self.config.max_entries :]:
            if path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                _remove_directory(path)


def _remove_directory(path: Path) -> None:
    for child in path.iterdir():
        if child.is_file():
            child.unlink(missing_ok=True)
        else:
            _remove_directory(child)
    os.rmdir(path)
