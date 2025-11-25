"""DearPyGui main window implementation for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import dearpygui.dearpygui as dpg

from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass
class CerebrusUI:
    """Composes a minimal Cerebrus DearPyGui window."""

    def __post_init__(self) -> None:
        self.icon_path = Path(__file__).resolve().parent.parent / "resources" / "icon.png"
        self.window_alias = "cerebrus_window"
        self.window_tag: int | None = None

    def _create_viewport(self) -> None:
        LOGGER.info("Creating viewport for Cerebrus window")
        dpg.create_context()
        self.window_tag = dpg.generate_uuid()
        dpg.create_viewport(
            title="Cerebrus Perf Report UE Toolkit",
            width=1600,
            height=900,
            small_icon=str(self.icon_path),
            large_icon=str(self.icon_path),
        )

    def _render_window(self) -> None:
        if self.window_tag is None:
            msg = "Viewport must be created before rendering the window"
            raise RuntimeError(msg)

        with dpg.window(
            tag=self.window_tag,
            alias=self.window_alias,
            label="Cerebrus Perf Report UE Toolkit",
            width=1580,
            height=880,
        ):
            dpg.add_spacer(height=20)
            dpg.add_text("Cerebrus UI placeholder")
            dpg.add_text("This build intentionally removes all functionality while the UI shell is being set up.")
        dpg.set_primary_window(self.window_tag, True)

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
