from __future__ import annotations

import os
import time
from pathlib import Path

from cerebrus.cache import CacheManager
from cerebrus.config.models import CacheConfig


def _touch(path: Path, timestamp: float) -> None:
    path.write_text("data")
    os.utime(path, (timestamp, timestamp))


def test_ensure_cache_creates_directory(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    manager = CacheManager(CacheConfig(directory=cache_dir, max_entries=5))

    created = manager.ensure_cache()

    assert created == cache_dir
    assert cache_dir.exists()
    assert cache_dir.is_dir()


def test_enforce_max_entries_evicts_oldest(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    now = time.time()
    older = cache_dir / "older.txt"
    newest = cache_dir / "newest.txt"
    middle = cache_dir / "middle.txt"

    _touch(older, now)
    _touch(middle, now + 5)
    _touch(newest, now + 10)

    manager = CacheManager(CacheConfig(directory=cache_dir, max_entries=2))

    manager.ensure_cache()

    remaining = {path.name for path in cache_dir.iterdir()}
    assert remaining == {"middle.txt", "newest.txt"}
