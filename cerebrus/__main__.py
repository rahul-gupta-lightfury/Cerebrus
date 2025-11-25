"""Entry-point for running Cerebrus via ``python -m cerebrus``."""

from __future__ import annotations

from cerebrus.core.app import CerebrusApp
from cerebrus.core.logging import configure_logging


def main() -> int:
    """Bootstrap the Cerebrus application scaffold."""
    configure_logging()
    app = CerebrusApp()
    app.initialize()
    app.run()
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution path
    raise SystemExit(main())
