"""Composable DearPyGui building blocks."""
from __future__ import annotations

from pathlib import Path

import dearpygui.dearpygui as dpg

from cerebrus.core.devices import DeviceInfo, collect_device_info
from cerebrus.ui.state import UIState

SELECTED_ROW_COLOR = (70, 130, 200, 90)
LOG_LEVEL_COLORS = {
    "DEBUG": (170, 170, 170),
    "INFO": (120, 200, 255),
    "WARNING": (255, 210, 120),
    "ERROR": (255, 120, 120),
    "SUCCESS": (15, 240, 15),
}


def build_menu_bar(state: UIState) -> None:
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
            dpg.add_menu_item(label="New", callback=lambda: _show_profile_dialog(state, is_edit=False))
            dpg.add_menu_item(label="Open", callback=lambda: _show_file_dialog("open_profile_dialog"))
            dpg.add_menu_item(label="Save", callback=lambda: _save_current_profile(state))
            dpg.add_menu_item(label="Edit", callback=lambda: _show_profile_dialog(state, is_edit=True))

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
        dpg.add_input_text(tag="profile_nickname_input", default_value=state.profile_nickname, width=120, readonly=True)
        dpg.add_text("ProfilePath:")
        dpg.add_input_text(tag="profile_path_input", default_value=str(state.profile_path), width=250, readonly=True)
        dpg.add_text("Package Name:")
        dpg.add_input_text(
            tag="package_input",
            default_value=state.package_name,
            width=180,
            readonly=True,
        )
        # Initial width adjustment for profile path
        _update_profile_path_display(state.profile_path)


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
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=240):
        dpg.add_text("Data and Perf Report", color=(120, 180, 255))
        with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=300)
            dpg.add_table_column(init_width_or_weight=1)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=200)

            with dpg.table_row():
                dpg.add_text("Output file Name:")
                dpg.add_input_text(
                    tag="output_file_name",
                    default_value=state.output_file_name,
                    width=220,
                )
                dpg.add_checkbox(
                    tag="use_prefix_only",
                    label="Use as Prefix only",
                    default_value=state.use_prefix_only,
                    callback=_handle_use_prefix_toggle,
                    user_data=state,
                )

            with dpg.table_row():
                dpg.add_text("Copy Directory /Input File/Folder Path:")
                with dpg.group(horizontal=True, horizontal_spacing=8):
                    dpg.add_input_text(
                        tag="input_path_label",
                        default_value=str(state.input_path),
                        width=320,
                        readonly=True,
                    )
                    dpg.add_button(
                        label="Browse",
                        width=90,
                        callback=lambda: _show_file_dialog("input_path_dialog"),
                    )
                dpg.add_spacer(width=10)

            with dpg.table_row():
                dpg.add_text("Output Folder Path:")
                with dpg.group(horizontal=True, horizontal_spacing=8):
                    dpg.add_input_text(
                        tag="output_path_label",
                        default_value=str(state.output_path),
                        width=320,
                        readonly=True,
                    )
                    dpg.add_button(
                        label="Browse",
                        width=90,
                        callback=lambda: _show_file_dialog("output_path_dialog"),
                    )
                dpg.add_spacer(width=10)

        with dpg.group(horizontal=True, horizontal_spacing=12):
            with dpg.child_window(border=True, autosize_y=True, width=260):
                dpg.add_text("From Phone to PC", color=(200, 200, 200))
                dpg.add_button(label="Copy logs", width=200)
                dpg.add_button(label="Copy CSV data", width=200)

            with dpg.child_window(border=True, autosize_y=True, width=260):
                dpg.add_text("From PC TO PC", color=(200, 200, 200))
                dpg.add_button(label="Stub Action 1", width=200)
                dpg.add_button(label="Stub Action 2", width=200)
                dpg.add_button(label="Stub Action 3", width=200)

    dpg.add_separator()
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=200):
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

    _register_file_dialogs(state)


def _populate_devices(state: UIState) -> None:
    package_value = dpg.get_value("package_input") if dpg.does_item_exist("package_input") else ""
    state.package_name = package_value or ""
    state.devices = collect_device_info(state.package_name)
    _refresh_device_table(state)


def _handle_log_filter(sender: int, app_data: str, user_data: UIState) -> None:
    user_data.log_filter = app_data or ""
    _render_log_entries(user_data)


def _handle_use_prefix_toggle(sender: int, app_data: bool, user_data: UIState) -> None:
    user_data.use_prefix_only = bool(app_data)


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


def _show_file_dialog(tag: str) -> None:
    if dpg.does_item_exist(tag):
        dpg.configure_item(tag, show=True)


def _register_file_dialogs(state: UIState) -> None:
    if not dpg.does_item_exist("input_path_dialog"):
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=_handle_input_path_selected,
            user_data=state,
            tag="input_path_dialog",
            width=600,
            height=400,
        ):
            dpg.add_file_extension(".csv", color=(0, 120, 255, 255))
            dpg.add_file_extension(".*")

    if not dpg.does_item_exist("output_path_dialog"):
        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            callback=_handle_output_path_selected,
            user_data=state,
            tag="output_path_dialog",
            width=500,
            height=400,
        ):
            dpg.add_file_extension(".*")

    if not dpg.does_item_exist("open_profile_dialog"):
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=_handle_open_profile_selected,
            user_data=state,
            tag="open_profile_dialog",
            width=600,
            height=400,
        ):
            dpg.add_file_extension(".json", color=(0, 255, 0, 255))
            dpg.add_file_extension(".*")


def _handle_input_path_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = next(iter(app_data.get("selections", {}).values()), None)
    if selection is None:
        return

    user_data.input_path = Path(selection)
    if dpg.does_item_exist("input_path_label"):
        dpg.set_value("input_path_label", str(selection))


    user_data.output_path = Path(selection)
    if dpg.does_item_exist("output_path_label"):
        dpg.set_value("output_path_label", str(selection))


def _handle_output_path_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = app_data.get("file_path_name") or next(iter(app_data.get("selections", {}).values()), None)
    if selection is None:
        return

    user_data.output_path = Path(selection)
    if dpg.does_item_exist("output_path_label"):
        dpg.set_value("output_path_label", str(selection))


def _handle_package_name_change(sender: int, app_data: str, user_data: UIState) -> None:
    user_data.package_name = app_data
    # Validation logic
    if not app_data.startswith("com."):
        # We could show an error, or just let it be invalid until save?
        # User said "cannot be null and must start with com."
        # We can change text color to red if invalid?
        dpg.configure_item(sender, user_data=user_data) # Trigger update?
        pass


def _show_profile_dialog(state: UIState, is_edit: bool = False) -> None:
    if is_edit:
        # Check if default profile
        if not state.profile_manager.current_profile_path:
             # Show warning
             if not dpg.does_item_exist("default_profile_warning"):
                 with dpg.window(tag="default_profile_warning", label="Warning", modal=True, width=400, height=150):
                     dpg.add_text("Cannot edit the Default Profile.\nPlease create a New Profile or Open an existing one.")
                     dpg.add_button(label="OK", width=100, callback=lambda: dpg.delete_item("default_profile_warning"))
             return

    if dpg.does_item_exist("profile_dialog"):
        dpg.delete_item("profile_dialog")

    title = "Edit Profile" if is_edit else "New Profile"
    
    # Pre-fill values if editing
    profile = state.profile_manager.current_profile
    engine_root = profile.engine_root if is_edit and profile else ""
    project_root = profile.project_root if is_edit and profile else ""
    nickname = profile.nickname if is_edit and profile else ""
    package_name = state.package_name if is_edit else ""

    with dpg.window(tag="profile_dialog", label=title, modal=True, width=500, height=250):
        with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(init_width_or_weight=1)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=50)

            with dpg.table_row():
                dpg.add_text("Profile Name:")
                dpg.add_input_text(tag="pd_nickname", default_value=nickname or "")
                dpg.add_spacer()

            with dpg.table_row():
                dpg.add_text("Package Name:")
                dpg.add_input_text(tag="pd_package_name", default_value=package_name)
                dpg.add_spacer()

        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=lambda: _handle_profile_save(state))
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("profile_dialog"))
    
    # Register dialogs for this modal
    _register_profile_file_dialogs(state)


def _handle_profile_save(state: UIState) -> None:
    package_name = dpg.get_value("pd_package_name")
    nickname = dpg.get_value("pd_nickname")

    # Validation
    if not package_name.startswith("com."):
        # Show error
        # For now just print or ignore
        print("Invalid Package Name") 
        return

    # If new, we need a path to save to. 
    # For now, let's just save to a default location or ask?
    # The reference image doesn't show a path selector for the profile itself, 
    # but "Profile Path" is in the main UI.
    # If "New", we probably need to ask where to save the JSON.
    
    # Let's close the dialog and ask for save location if it's new.
    # Or if it's edit, just save.
    
    dpg.delete_item("profile_dialog")
    
    # Update state
    state.package_name = package_name
    if dpg.does_item_exist("package_input"):
        dpg.set_value("package_input", package_name)
    
    # Create/Update profile object
    # If we don't have a current profile path, we need to ask for one.
    if not state.profile_manager.current_profile_path:
         _show_file_dialog("save_profile_as_dialog")
         # We need to store the temp values somewhere to save them after path selection
         state.temp_profile_data = {
             "nickname": nickname,
             "package_name": package_name,
         }
    else:
        # Update existing
        profile = state.profile_manager.current_profile
        if profile:
            profile.nickname = nickname
            profile.package_name = package_name
            state.profile_manager.save_current_profile()
            state.profile_nickname = nickname or "None"
            # Refresh UI
            if dpg.does_item_exist("profile_nickname_input"):
                dpg.set_value("profile_nickname_input", state.profile_nickname)
            pass


def _save_current_profile(state: UIState) -> None:
    if state.profile_manager.current_profile and state.profile_manager.current_profile_path:
        # Update profile from current UI state
        state.profile_manager.current_profile.package_name = state.package_name
        # Update other fields if we track them
        state.profile_manager.save_current_profile()
    else:
        _show_file_dialog("save_profile_as_dialog")


def _register_profile_file_dialogs(state: UIState) -> None:
    if not dpg.does_item_exist("save_profile_as_dialog"):
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=_handle_save_profile_as_selected,
            user_data=state,
            tag="save_profile_as_dialog",
            width=500,
            height=400,
            default_filename="profile.json",
        ):
             dpg.add_file_extension(".json", color=(0, 255, 0, 255))


def _handle_save_profile_as_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = app_data.get("file_path_name") or next(iter(app_data.get("selections", {}).values()), None)
    if not selection:
        return
    
    path = Path(selection)
    if not path.suffix:
        path = path.with_suffix(".json")
    
    # Retrieve temp data if we came from the dialog
    temp_data = getattr(user_data, "temp_profile_data", {})
    
    nickname = temp_data.get("nickname")
    package_name = temp_data.get("package_name") or user_data.package_name
    
    # Create profile
    profile = user_data.profile_manager.create_new_profile(
        nickname=nickname,
        package_name=package_name,
        path=path
    )
    profile.save(path)
    
    # Update UI
    user_data.profile_nickname = nickname or "None"
    user_data.package_name = package_name
    user_data.profile_path = path
    
    if dpg.does_item_exist("profile_nickname_input"):
        dpg.set_value("profile_nickname_input", nickname or "None")
    if dpg.does_item_exist("profile_path_input"):
        dpg.set_value("profile_path_input", str(path))
        _update_profile_path_display(path)
    if dpg.does_item_exist("package_input"):
        dpg.set_value("package_input", package_name)


def _handle_open_profile_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = next(iter(app_data.get("selections", {}).values()), None)
    if selection:
        path = Path(selection)
        try:
            profile = user_data.profile_manager.load_last_profile() # Wait, this loads last. We want to load specific.
            # We need a method to load specific in manager.
            # Let's just load it manually here for now or add method to manager.
            # Accessing private/internal logic of manager is okay-ish.
            from cerebrus.core.profile import Profile
            profile = Profile.load(path)
            user_data.profile_manager.current_profile = profile
            user_data.profile_manager.current_profile_path = path
            user_data.profile_manager.set_last_used_profile_path(path)
            
            # Update UI
            user_data.profile_nickname = profile.nickname or "None"
            user_data.package_name = profile.package_name
            user_data.profile_path = path
            
            if dpg.does_item_exist("package_input"):
                dpg.set_value("package_input", profile.package_name)
            
            if dpg.does_item_exist("profile_nickname_input"):
                dpg.set_value("profile_nickname_input", profile.nickname or "None")
            
            if dpg.does_item_exist("profile_path_input"):
                dpg.set_value("profile_path_input", str(path))
                _update_profile_path_display(path)
            
        except Exception as e:
            print(f"Error loading profile: {e}")


def _update_profile_path_display(path: Path) -> None:
    if not dpg.does_item_exist("profile_path_input"):
        return
    
    path_str = str(path)
    # Approximate width: char count * 7 pixels (approx for default font) + padding
    # Clamp between min and max if needed, or just let it grow.
    new_width = max(250, len(path_str) * 7 + 20)
    dpg.configure_item("profile_path_input", width=new_width)


