"""Configuration panel stub."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState

LOGGER = get_logger(__name__)


@dataclass
class ConfigPanel:
    state: ApplicationState

    def render(self) -> None:
        LOGGER.info(
            "Config panel exposing %d profiles", len(self.state.config.profiles)
        )
