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
            "Config panel ready (tool paths: uaft=%s, csvtools=%s)",
            self.state.config.tool_paths.uaft,
            self.state.config.tool_paths.csvtools_root,
        )
