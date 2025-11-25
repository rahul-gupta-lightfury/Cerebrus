"""DearPyGui application entry point."""
from __future__ import annotations

from pathlib import Path

import dearpygui.dearpygui as dpg

from cerebrus.ui import components
from cerebrus.ui.state import UIState


class CerebrusApp:
    """Build and run the Cerebrus UI described in the sketch."""

    def __init__(self, state: UIState | None = None) -> None:
        self.state = state or UIState()

    def build(self) -> None:
        dpg.create_context()
        self.state.package_name = "com.lightfury.titan"
        with dpg.window(tag="MainWindow", label="Cerebrus - An Unreal Engine Perf Report UI Toolkit", width=1100, height=750):
            components.build_menu_bar()
            components.build_profile_summary(self.state)
            components.build_device_controls(self.state)
            components.build_file_actions(self.state)

        dpg.set_primary_window("MainWindow", True)

    def run(self) -> None:
        self.build()
        resources_dir = Path(__file__).resolve().parent.parent / "resources"
        small_icon_path = resources_dir / "icon64x64.ico"
        large_icon_path = resources_dir / "icon256x256.ico"
        dpg.create_viewport(
            title="Cerebrus",
            width=1200,
            height=800,
            small_icon=str(small_icon_path),
            large_icon=str(large_icon_path),
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
