"""DearPyGui main window implementation for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import dearpygui.dearpygui as dpg

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
from cerebrus.ui.layout import ContentTabs, MenuBar, ProfileBar

LOGGER = get_logger(__name__)


@dataclass
class CerebrusUI:
    """Composes the Cerebrus DearPyGui window."""

    state: ApplicationState
    device_manager: DeviceManager

    def __post_init__(self) -> None:
        self.menu_bar = MenuBar(tag="cerebrus_menu")
        self.profile_bar = ProfileBar(state=self.state, tag="profile_bar")
        self.tabs = ContentTabs(state=self.state)
        self.icon_path = Path(__file__).resolve().parent.parent / "resources" / "icon.png"

    def _create_viewport(self) -> None:
        LOGGER.info("Creating viewport for Cerebrus window")
        dpg.create_context()
        dpg.create_viewport(
            title="Cerebrus",
            width=1600,
            height=900,
            small_icon=str(self.icon_path),
            large_icon=str(self.icon_path),
        )

    def _render_window(self) -> None:
        with dpg.window(tag="cerebrus_window", label="Cerebrus", width=1580, height=880):
            self.menu_bar.render()
            self.profile_bar.render()
            self.tabs.render()
        dpg.set_primary_window("cerebrus_window", True)

    def render_once(self) -> None:
        """Render and run the Cerebrus DearPyGui UI."""
        LOGGER.info("Rendering Cerebrus UI window")
        self._create_viewport()
        self._render_window()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()
