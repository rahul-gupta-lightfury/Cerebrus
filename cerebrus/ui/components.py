"""Composable DearPyGui building blocks."""
from __future__ import annotations

import dearpygui.dearpygui as dpg

from cerebrus.core.devices import DeviceInfo, collect_device_info
from cerebrus.ui.state import UIState

SELECTED_ROW_COLOR = (70, 130, 200, 90)
LOG_LEVEL_COLORS = {
    "DEBUG": (170, 170, 170),
    "INFO": (120, 200, 255),
    "WARNING": (255, 210, 120),
    "ERROR": (255, 120, 120),
}


def build_menu_bar() -> None:
    """Render the top menu bar."""
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New Window", shortcut="Ctrl+N")
            dpg.add_menu_item(label="Exit Window", shortcut="Alt+F4")

        with dpg.menu(label="View"):
            dpg.add_menu_item(label="Reset Layout")

        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Echo Test Command")

        with dpg.menu(label="Profile"):
            dpg.add_menu_item(label="New")
            dpg.add_menu_item(label="Open")
            dpg.add_menu_item(label="Save")
            dpg.add_menu_item(label="Edit")

        with dpg.menu(label="Settings"):
            with dpg.menu(label="Load Theme"):
                dpg.add_menu_item(label="System Color")
                dpg.add_menu_item(label="Dark")
                dpg.add_menu_item(label="Light")
                dpg.add_menu_item(label="Create Custom")
                dpg.add_separator()
                dpg.add_menu_item(
                    label=(
                        "Auto populate later when theme system is added from themes saved in a "
                        "fixed directory"
                    )
                )

            with dpg.menu(label="Log Colors"):
                dpg.add_menu_item(label="Edit")
                dpg.add_menu_item(label="Import")
                dpg.add_menu_item(label="Export")
                dpg.add_separator()
                dpg.add_menu_item(label="Reset to Defaults")

            with dpg.menu(label="Key Bindings"):
                dpg.add_menu_item(label="Edit")
                dpg.add_menu_item(label="Import")
                dpg.add_menu_item(label="Export")
                dpg.add_separator()
                dpg.add_menu_item(label="Reset to Defaults")

        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="Help")
            dpg.add_menu_item(label="Provide Feedback")
            dpg.add_menu_item(label="About")


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
    """Render file copy actions and reporting panels."""
    dpg.add_separator()
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=140):
        dpg.add_text("Data", color=(120, 180, 255))
        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_button(label="Copy logs", width=120)
            dpg.add_button(label="Copy CSV data", width=140)

        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_text("Copy Location:")
            dpg.add_input_text(default_value=str(state.copy_directory), width=350)
            dpg.add_button(label="Browse", width=100)

    dpg.add_separator()
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=260):
        dpg.add_text("Perf Report", color=(120, 180, 255))
        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_text("Output file Name:")
            dpg.add_input_text(
                tag="output_file_name",
                default_value=state.output_file_name,
                width=200,
            )
            dpg.add_checkbox(
                tag="use_prefix_only",
                label="Use as Prefix only",
                default_value=state.use_prefix_only,
            )

        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_text("Input File/Folder Path:")
            dpg.add_input_text(
                tag="input_path_label",
                default_value=str(state.input_path),
                width=350,
                readonly=True,
            )
            dpg.add_button(label="Browse", width=100)

        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_text("Output Folder Path:")
            dpg.add_input_text(
                tag="output_path_label",
                default_value=str(state.output_path),
                width=350,
                readonly=True,
            )
            dpg.add_button(label="Browse", width=100)

        dpg.add_separator()

        dpg.add_text("Logging", color=(120, 180, 255))
        dpg.add_input_text(
            tag="log_filter_input",
            label="Filter",
            width=280,
            callback=_handle_log_filter,
            user_data=state,
        )
        with dpg.child_window(border=True, autosize_x=True, height=130, tag="log_container"):
            _render_log_entries(state)


def _populate_devices(state: UIState) -> None:
    package_value = dpg.get_value("package_input") if dpg.does_item_exist("package_input") else ""
    state.package_name = package_value or ""
    state.devices = collect_device_info(state.package_name)
    _refresh_device_table(state)


def _handle_log_filter(sender: int, app_data: str, user_data: UIState) -> None:
    user_data.log_filter = app_data or ""
    _render_log_entries(user_data)


def _render_log_entries(state: UIState) -> None:
    if not dpg.does_item_exist("log_container"):
        return

    dpg.delete_item("log_container", children_only=True)
    filter_value = state.log_filter.lower()
    filtered_logs = [
        entry
        for entry in state.logs
        if filter_value in entry[0].lower() or filter_value in entry[1].lower()
    ]

    if not filtered_logs:
        dpg.add_text(
            "No log entries match the filter.",
            color=(180, 180, 180),
            parent="log_container",
        )
        return

    for level, message in filtered_logs:
        color = LOG_LEVEL_COLORS.get(level.upper(), (220, 220, 220))
        dpg.add_text(f"[{level}] {message}", color=color, parent="log_container")


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

        state.device_cell_tags = []

        if not state.devices:
            with dpg.table_row():
                for message in ["-", "-", "No devices listed", "-", "-", "-"]:
                    dpg.add_text(message)
        else:
            for row_index, device in enumerate(state.devices):
                _render_device_row(row_index, device, state)


def _render_device_row(row_index: int, device: DeviceInfo, state: UIState) -> None:
    with dpg.table_row():
        values = [
            device.make,
            device.model,
            device.serial,
            device.android_version,
            device.sdk_level,
            "True" if device.package_found else "False",
        ]

        row_tags: list[str] = []
        for column_index, value in enumerate(values):
            cell_tag = f"device_cell_{row_index}_{column_index}"
            dpg.add_selectable(
                tag=cell_tag,
                label=value,
                span_columns=False,
                callback=_handle_device_select,
                user_data=(state, row_index, device.serial),
            )
            row_tags.append(cell_tag)

        state.device_cell_tags.append(row_tags)

    if state.selected_device_serial == device.serial:
        _select_device_row(row_index, state)


def _handle_device_select(sender: int, app_data: int, user_data: tuple[UIState, int, str]) -> None:
    state, row_index, serial = user_data
    state.selected_device_serial = serial

    if not dpg.does_item_exist("device_table"):
        return
    _select_device_row(row_index, state)


def _select_device_row(row_index: int, state: UIState) -> None:
    for index in range(len(state.devices)):
        dpg.unhighlight_table_row("device_table", index)

    dpg.highlight_table_row("device_table", row_index, SELECTED_ROW_COLOR)

    for cell_tags in state.device_cell_tags:
        for tag in cell_tags:
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, False)

    if 0 <= row_index < len(state.device_cell_tags):
        for tag in state.device_cell_tags[row_index]:
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, True)
