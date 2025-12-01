"""Run lightweight validation before launching the UI."""

from __future__ import annotations

from pathlib import Path

from cerebrus.cache import CacheManager
from cerebrus.config.loader import load_config_from_file


def run_preflight(config_path: Path | None = None) -> Path:
    """Validate configuration and ensure the cache directory exists.

    Returns the path to the cache directory created or refreshed.
    """

    config_location = config_path or Path("config/cerebrus.yaml")
    config = load_config_from_file(config_location)
    cache_manager = CacheManager(config.cache)
    return cache_manager.ensure_cache()


if __name__ == "__main__":  # pragma: no cover - manual entry point
    created = run_preflight()
    print(f"Cache verified at: {created}")
