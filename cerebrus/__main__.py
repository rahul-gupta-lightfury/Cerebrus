"""Entry-point for running Cerebrus via ``python -m cerebrus``."""

from __future__ import annotations

from typing import Sequence

from cerebrus.core.app import CerebrusApp
from cerebrus.core.config_loader import ConfigLoader
from cerebrus.core.logging import configure_logging


def _build_app() -> CerebrusApp:
    """Create and initialize the core application."""

    configure_logging()
    loader = ConfigLoader()
    config = loader.load()
    app = CerebrusApp(config=config)
    app.initialize()
    return app


def main(argv: Sequence[str] | None = None) -> int:
    """Launch the Dear PyGui dashboard for the scaffold."""

    _ = argv  # CLI arguments are reserved for future use
    app = _build_app()
    app.run()
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution path
    raise SystemExit(main())
