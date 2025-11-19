"""UI scaffold built on top of Dear ImGui."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
from cerebrus.ui.device_panel import DevicePanel
from cerebrus.ui.capture_panel import CapturePanel
from cerebrus.ui.report_panel import ReportPanel
from cerebrus.ui.config_panel import ConfigPanel

LOGGER = get_logger(__name__)


@dataclass
class CerebrusUI:
    """Aggregates the individual Dear ImGui panels."""

    state: ApplicationState
    device_manager: DeviceManager

    def __post_init__(self) -> None:
        self.device_panel = DevicePanel(device_manager=self.device_manager)
        self.capture_panel = CapturePanel(state=self.state)
        self.report_panel = ReportPanel(state=self.state)
        self.config_panel = ConfigPanel(state=self.state)

    def render_once(self) -> None:
        LOGGER.info("Rendering UI scaffold")
        self.device_panel.render()
        self.capture_panel.render()
        self.report_panel.render()
        self.config_panel.render()
