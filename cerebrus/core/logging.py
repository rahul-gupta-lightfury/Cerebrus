"""Central logging configuration for Cerebrus."""

from __future__ import annotations

import logging
from logging import Logger

_LOGGER_NAME = "cerebrus"


def configure_logging(level: int | None = None) -> Logger:
    """Configure and return the root Cerebrus logger."""
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level or logging.INFO)
    return logger


def get_logger(name: str) -> Logger:
    """Return a child logger scoped beneath the Cerebrus root logger."""
    return logging.getLogger(f"{_LOGGER_NAME}.{name}")
