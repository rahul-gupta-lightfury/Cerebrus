"""Lightweight preflight checks for CI and local validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from cerebrus.cache import CacheManager
from cerebrus.config import defaults
from cerebrus.config.loader import load_config_from_file
from cerebrus.core.logging import configure_logging, get_logger

LOGGER = get_logger(__name__)


def run_preflight(config_path: Path | None = None) -> Path:
    """Run minimal preflight checks and return the cache directory.

    If *config_path* does not exist, the default configuration is loaded.
    The cache directory is created and trimmed according to the configured
    retention policy.
    """

    selected_path = config_path or defaults.DEFAULT_CONFIG_PATH
    config = load_config_from_file(selected_path)
    cache_manager = CacheManager(config=config.cache)
    cache_dir = cache_manager.ensure_cache()
    LOGGER.info("Preflight completed with cache at %s", cache_dir)
    return cache_dir


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Cerebrus preflight checks")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional path to a cerebrus.yaml config file (defaults to config/cerebrus.yaml)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = _parse_args(argv)
    try:
        run_preflight(args.config)
    except Exception as exc:  # pragma: no cover - safety net for CLI usage
        LOGGER.error("Preflight failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
