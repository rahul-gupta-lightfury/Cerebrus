"""Report panel stub."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState

LOGGER = get_logger(__name__)


@dataclass
class ReportPanel:
    state: ApplicationState

    def render(self) -> None:
        LOGGER.info(
            "Report panel would render reports for cache dir %s",
            self.state.cache_directory,
        )
