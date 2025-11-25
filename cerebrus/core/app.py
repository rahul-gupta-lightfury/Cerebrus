"""Application lifecycle glue for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass, field

from cerebrus.config.models import CerebrusConfig
from cerebrus.core.logging import get_logger
from cerebrus.ui.main_window import CerebrusUI

LOGGER = get_logger(__name__)


@dataclass
class CerebrusApp:
    """Minimal Cerebrus application lifecycle."""

    config: CerebrusConfig

    def __post_init__(self) -> None:
        self.ui = CerebrusUI()

    def initialize(self) -> None:
        LOGGER.info("Skipping initialization; rendering placeholder UI only.")

    def run(self) -> None:
        LOGGER.info("Running Cerebrus placeholder UI")
        self.ui.render_once()
