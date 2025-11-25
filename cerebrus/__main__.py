"""Entry-point for running Cerebrus via ``python -m cerebrus``."""

from __future__ import annotations

from pathlib import Path

from cerebrus.core.app import CerebrusApp
from cerebrus.core.config_loader import ConfigLoader
from cerebrus.core.logging import configure_logging


def main() -> int:
    """Bootstrap the Cerebrus application scaffold."""
    configure_logging()
    loader = ConfigLoader()
    config = loader.load()
    app = CerebrusApp(config=config)
    app.initialize()
    app.run()
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution path
    raise SystemExit(main())
