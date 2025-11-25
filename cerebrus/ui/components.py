"""Composable DearPyGui building blocks."""
from __future__ import annotations

import dearpygui.dearpygui as dpg

from cerebrus.core.devices import DeviceInfo, collect_device_info
from cerebrus.ui.state import UIState


MENU_LABELS = ["File", "View", "Tools", "Profile", "Settings", "Help"]


def build_menu_bar() -> None:
    """Render the top menu bar."""
    with dpg.menu_bar():
        for label in MENU_LABELS:
            dpg.add_menu(label=label)


def build_profile_summary(state: UIState) -> None:
    """Render the profile summary strip with read-only inputs."""
    with dpg.group(horizontal=True, horizontal_spacing=12):
        dpg.add_text("Profile:")
        dpg.add_input_text(default_value=state.profile_nickname, width=120, readonly=True)
        dpg.add_text("ProfilePath:")
        dpg.add_input_text(default_value=str(state.profile_path), width=250, readonly=True)
        dpg.add_text("Package Name:")
        dpg.add_input_text(tag="package_input", default_value=state.package_name, width=180)


def build_device_controls(state: UIState) -> None:
    """Render device actions and the device table container."""
    dpg.add_separator()
    with dpg.group(horizontal=True, horizontal_spacing=8):
        dpg.add_text("Device(s)", color=(120, 180, 255))
        dpg.add_button(label="List Devices", width=120, callback=lambda: _populate_devices(state))

    with dpg.child_window(border=False, autosize_x=True, height=220, tag="device_table_container"):
        _render_device_table(state)


def build_file_actions(state: UIState) -> None:
    """Render the date, copy actions, and report trigger."""
    dpg.add_separator()
    with dpg.group(horizontal=True, horizontal_spacing=10):
        dpg.add_text("Date:")
        dpg.add_input_text(default_value=state.date_string, width=120)
        dpg.add_button(label="Copy logs", width=100)
        dpg.add_button(label="Copy CSV data", width=120)
        dpg.add_button(label="Copy CSV data", width=120)
        dpg.add_text("->")
        dpg.add_button(label="Browse", width=100)

    with dpg.group(horizontal=True, horizontal_spacing=10):
        dpg.add_text("Copy Dir:")
        dpg.add_input_text(default_value=str(state.copy_directory), width=350)
        dpg.add_button(label="Browse", width=100)

    dpg.add_button(label="Text Report", width=120)


def _populate_devices(state: UIState) -> None:
    package_value = dpg.get_value("package_input") if dpg.does_item_exist("package_input") else ""
    state.package_name = package_value or ""
    state.devices = collect_device_info(state.package_name)
    _refresh_device_table(state)


def _refresh_device_table(state: UIState) -> None:
    if not dpg.does_item_exist("device_table_container"):
        return

    existing_table = "device_table"
    if dpg.does_item_exist(existing_table):
        dpg.delete_item(existing_table)

    _render_device_table(state)


def _render_device_table(state: UIState) -> None:
    with dpg.table(
        tag="device_table",
        parent="device_table_container",
        header_row=True,
        resizable=True,
        borders_outerH=True,
        borders_outerV=True,
        borders_innerH=True,
        borders_innerV=True,
    ):
        for column in [
            "Make",
            "Model",
            "Serial",
            "Android Ver.",
            "SDK level",
            "Package Found",
        ]:
            dpg.add_table_column(label=column)

        if not state.devices:
            with dpg.table_row():
                for message in ["-", "-", "No devices listed", "-", "-", "-"]:
                    dpg.add_text(message)
        else:
            for device in state.devices:
                _render_device_row(device)


def _render_device_row(device: DeviceInfo) -> None:
    with dpg.table_row():
        values = [
            device.make,
            device.model,
            device.serial,
            device.android_version,
            device.sdk_level,
            "True" if device.package_found else "False",
        ]
        for value in values:
            dpg.add_text(value)
