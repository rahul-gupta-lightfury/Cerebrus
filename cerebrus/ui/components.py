"""Composable DearPyGui building blocks."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import dearpygui.dearpygui as dpg

from cerebrus.core.devices import DeviceInfo, collect_device_info
from cerebrus.tools.adb import AdbClient, AdbError
from cerebrus.ui.state import UIState

SELECTED_ROW_COLOR = (70, 130, 200, 90)
LOG_LEVEL_COLORS = {
    "DEBUG": (170, 170, 170),
    "INFO": (120, 200, 255),
    "WARNING": (255, 210, 120),
    "ERROR": (255, 120, 120),
    "SUCCESS": (15, 240, 15),
}

# Tooltip definitions
TOOLTIPS = {
    "output_file_name": "The name to use for output files. This will be used as the filename or prefix depending on the 'Use as Prefix only' setting.",
    "use_prefix_only": "When enabled, the Output File Name will be used as a prefix with device-specific information appended. When disabled, it will be used as the exact filename.",
    "input_path": "The folder path where files will be moved from the device. CSV and Logs subfolders will be created here.",
    "output_path": "The destination folder where processed reports and logs will be saved.",
    "append_device": "When enabled, a subfolder with the device make and model will be automatically created in the output path.",
    "move_logs": "Moves log files from the selected device's Unreal Engine Saved/Logs folder to your PC.",
    "move_csv": "Moves CSV profiling data from the selected device's Unreal Engine Saved/Profiling/CSV folder to your PC.",
    "generate_perf": "Processes CSV files in the Move Files Folder Path using PerfreportTool.exe and generates performance reports in the Output Folder Path. CSV files are deleted after successful processing.",
    "generate_logs": "Converts text log files (.log, .txt) from the Move Files Folder Path to colored HTML format in the Output Folder Path. Source files are deleted after successful conversion.",
    "generate_both": "Runs both Perf Report generation and Colored Logs conversion in sequence.",
    "package_name": "The Android package identifier for your application (e.g., com.company.appname). Must start with 'com.' and have at least 3 parts.",
    "device_table": "Lists all connected Android devices. Select a device to perform operations. Only devices with the package installed can be selected.",
    "list_devices": "Scans for connected Android devices via ADB and checks if the specified package is installed on each device.",
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
            dpg.add_menu_item(label="Echo Test Command", callback=lambda: log_message(state, "INFO", "Echo Test Command Executed"))

        with dpg.menu(label="Profile"):
            dpg.add_menu_item(label="New", callback=lambda: _show_profile_dialog(state, is_edit=False))
            dpg.add_menu_item(label="Open", callback=lambda: _show_file_dialog("open_profile_dialog"))
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
        dpg.add_text("Profile Name:")
        # Use warning color for default profile, green for loaded profiles
        profile_color = (255, 210, 120) if not state.profile_manager.current_profile_path else (150, 255, 150)
        dpg.add_text(tag="profile_nickname_input", default_value=state.profile_nickname, color=profile_color)
        dpg.add_text("Package Name:")
        dpg.add_text(
            tag="package_input",
            default_value=state.package_name,
            color=profile_color,
        )
        _add_help_button("package_name")
        dpg.add_text("Profile Path:")
        dpg.add_text(tag="profile_path_input", default_value=str(state.profile_path), color=profile_color)


def build_device_controls(state: UIState) -> None:
    """Render device actions and the device table container."""
    dpg.add_separator()
    with dpg.group(horizontal=True, horizontal_spacing=8):
        dpg.add_text("Device(s)", color=(120, 180, 255))
        _add_help_button("device_table")
        dpg.add_button(label="List Devices", width=120, callback=lambda: _populate_devices(state))
        _add_help_button("list_devices")

    with dpg.child_window(border=False, autosize_x=True, height=220, tag="device_table_container"):
        _render_device_table(state)


def build_file_actions(state: UIState) -> None:
    """Render file copy actions and reporting panels."""
    dpg.add_separator()
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=240):
        dpg.add_text("Data and Perf Report", color=(120, 180, 255))
        with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=320)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=350)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=180)

            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_text("Output file Name:")
                    _add_help_button("output_file_name")
                dpg.add_input_text(
                    tag="output_file_name",
                    default_value=state.output_file_name,
                    width=-1,
                    callback=_handle_output_file_name_change,
                    user_data=state,
                )
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(
                        tag="use_prefix_only",
                        label="Use as Prefix only",
                        default_value=state.use_prefix_only,
                        callback=_handle_use_prefix_toggle,
                        user_data=state,
                    )
                    _add_help_button("use_prefix_only")

            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_text("Move Files Folder Path:")
                    _add_help_button("input_path")
                dpg.add_input_text(
                    tag="input_path_label",
                    default_value=str(state.input_path),
                    width=-1,
                    readonly=True,
                )
                dpg.add_button(
                    label="Browse",
                    width=-1,
                    callback=lambda: _show_file_dialog("input_path_dialog"),
                )

            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_text("Output Folder Path:")
                    _add_help_button("output_path")
                dpg.add_input_text(
                    tag="output_path_label",
                    default_value=str(state.output_path),
                    width=-1,
                    readonly=True,
                )
                dpg.add_button(
                    label="Browse",
                    width=-1,
                    callback=lambda: _show_file_dialog("output_path_dialog"),
                )

            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_text("Append Device Make and Model to Output Path:")
                    _add_help_button("append_device")
                dpg.add_spacer()
                dpg.add_checkbox(
                    tag="append_device_to_path",
                    label="",
                    default_value=False,
                    callback=_handle_append_device_toggle,
                    user_data=state,
                )

        with dpg.group(horizontal=True, horizontal_spacing=12):
            with dpg.child_window(border=True, autosize_y=True, width=360):
                dpg.add_text("Bulk Actions From Selected Phone to PC", color=(200, 200, 200))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Move logs", width=200, callback=lambda: _handle_move_logs(state))
                    _add_help_button("move_logs")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Move CSV data", width=200, callback=lambda: _handle_move_csv(state))
                    _add_help_button("move_csv")

            with dpg.child_window(border=True, autosize_y=True, width=420):
                dpg.add_text("Bulk Actions From PC to PC", color=(200, 200, 200))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Generate Perf Report Only", width=300, callback=lambda: _handle_generate_perf_report(state))
                    _add_help_button("generate_perf")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Generate Colored Logs Only", width=300, callback=lambda: _handle_generate_colored_logs(state))
                    _add_help_button("generate_logs")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Generate Perf Report + Colored Logs", width=300)
                    _add_help_button("generate_both")

    dpg.add_separator()
    with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=200):
        dpg.add_text("Logging", color=(120, 180, 255))
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="log_filter_input",
                label="Filter",
                width=280,
                callback=_handle_log_filter,
                user_data=state,
            )
            dpg.add_button(label="Clear", callback=lambda: _clear_logs(state))
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


def _handle_output_file_name_change(sender: int, app_data: str, user_data: UIState) -> None:
    user_data.output_file_name = app_data
    _auto_save_profile(user_data)


def _handle_use_prefix_toggle(sender: int, app_data: bool, user_data: UIState) -> None:
    user_data.use_prefix_only = bool(app_data)
    _auto_save_profile(user_data)


def _handle_append_device_toggle(sender: int, app_data: bool, user_data: UIState) -> None:
    user_data.append_device_to_path = bool(app_data)
    
    # Store base path if not already stored
    if user_data.base_output_path is None:
        user_data.base_output_path = user_data.output_path
    
    # Get the selected device
    selected_device = None
    if user_data.selected_device_serial:
        for device in user_data.devices:
            if device.serial == user_data.selected_device_serial:
                selected_device = device
                break
    
    if not selected_device:
        if app_data:
            log_message(user_data, "INFO", "Device Make/Model will be appended when a device is selected.")
        _auto_save_profile(user_data)
        return
    
    if app_data:  # Checkbox is checked
        # Append device make and model
        device_folder = f"{selected_device.make}_{selected_device.model}"
        new_path = user_data.base_output_path / device_folder
        user_data.output_path = new_path
        if dpg.does_item_exist("output_path_label"):
            dpg.set_value("output_path_label", str(new_path))
        log_message(user_data, "INFO", f"Output path updated: {new_path}")
    else:  # Checkbox is unchecked
        # Restore base path
        user_data.output_path = user_data.base_output_path
        if dpg.does_item_exist("output_path_label"):
            dpg.set_value("output_path_label", str(user_data.base_output_path))
        log_message(user_data, "INFO", f"Output path restored: {user_data.base_output_path}")
    
    _auto_save_profile(user_data)


def _handle_move_csv(state: UIState) -> None:
    _move_files_from_device(state, "Profiling/CSV", "CSV")


def _handle_move_logs(state: UIState) -> None:
    _move_files_from_device(state, "Logs", "Logs")


def _handle_generate_perf_report(state: UIState) -> None:
    """Run PerfreportTool on CSV files and delete them on success."""
    # Locate PerfreportTool.exe
    # Assuming repo root is 3 levels up from this file (cerebrus/ui/components.py -> cerebrus/ui -> cerebrus -> root)
    repo_root = Path(__file__).resolve().parent.parent.parent
    tool_path = repo_root / "Binaries" / "CsvTools" / "PerfreportTool.exe"

    if not tool_path.exists():
        log_message(state, "ERROR", f"PerfreportTool not found at: {tool_path}")
        return

    # Input CSV directory: {Move Files Folder Path}\CSV
    csv_dir = state.input_path / "CSV"
    if not csv_dir.exists():
        log_message(state, "ERROR", f"CSV directory not found: {csv_dir}")
        return

    # Output directory: {Output Folder Path}
    output_dir = state.output_path
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            log_message(state, "ERROR", f"Failed to create output directory: {e}")
            return

    csv_files = list(csv_dir.glob("*.csv"))
    if not csv_files:
        log_message(state, "WARNING", f"No CSV files found in {csv_dir}")
        return

    log_message(state, "INFO", f"Found {len(csv_files)} CSV files. Starting processing...")

    for csv_file in csv_files:
        # Construct command
        # Command: "{Tool}" -csv "{Input}" -reportType Default60fps -o "{Output}" -perfLog
        
        # Output path usually expects a filename prefix or full path. 
        # User specified: "{Ouput Folder Path}\{CSV File Name}"
        # We'll use the stem of the CSV file as the name.
        output_file_path = output_dir / csv_file.stem
        
        cmd = [
            str(tool_path),
            "-csv", str(csv_file),
            "-reportType", "Default60fps",
            "-o", str(output_file_path),
            "-perfLog"
        ]

        log_message(state, "INFO", f"Processing {csv_file.name}...")
        
        try:
            # Run command
            # Create startupinfo to hide console window on Windows
            startupinfo = None
            if hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )

            if result.returncode == 0:
                log_message(state, "SUCCESS", f"Generated report for {csv_file.name}")
                # Delete the CSV file
                try:
                    csv_file.unlink()
                    log_message(state, "INFO", f"Deleted {csv_file.name}")
                except Exception as e:
                    log_message(state, "WARNING", f"Failed to delete {csv_file.name}: {e}")
            else:
                log_message(state, "ERROR", f"Failed to process {csv_file.name}")
                log_message(state, "ERROR", f"Tool Output: {result.stdout}")
                log_message(state, "ERROR", f"Tool Error: {result.stderr}")

        except Exception as e:
            log_message(state, "ERROR", f"Exception while processing {csv_file.name}: {e}")

    log_message(state, "INFO", "Batch processing completed.")


def _handle_generate_colored_logs(state: UIState) -> None:
    """Convert text logs to colored HTML logs."""
    # Locate log_to_html.py
    repo_root = Path(__file__).resolve().parent.parent.parent
    tool_path = repo_root / "cerebrus" / "tools" / "log_to_html.py"

    if not tool_path.exists():
        log_message(state, "ERROR", f"Log conversion tool not found at: {tool_path}")
        return

    # Input Logs directory: {Move Files Folder Path}\Logs
    logs_dir = state.input_path / "Logs"
    if not logs_dir.exists():
        log_message(state, "ERROR", f"Logs directory not found: {logs_dir}")
        return

    # Output directory: {Output Folder Path}
    output_dir = state.output_path
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            log_message(state, "ERROR", f"Failed to create output directory: {e}")
            return

    log_files = list(logs_dir.glob("*.log")) + list(logs_dir.glob("*.txt"))
    if not log_files:
        log_message(state, "WARNING", f"No log files found in {logs_dir}")
        return

    log_message(state, "INFO", f"Found {len(log_files)} log files. Starting conversion...")

    for log_file in log_files:
        # Output HTML file path
        output_file_path = output_dir / f"{log_file.stem}.html"
        
        cmd = [
            sys.executable,
            str(tool_path),
            "-i", str(log_file),
            "-o", str(output_file_path),
        ]

        log_message(state, "INFO", f"Converting {log_file.name}...")
        
        try:
            # Run command
            startupinfo = None
            if hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )

            if result.returncode == 0:
                log_message(state, "SUCCESS", f"Created {output_file_path.name}")
                # Delete the source file
                try:
                    log_file.unlink()
                    log_message(state, "INFO", f"Deleted {log_file.name}")
                except Exception as e:
                    log_message(state, "WARNING", f"Failed to delete {log_file.name}: {e}")
            else:
                log_message(state, "ERROR", f"Failed to convert {log_file.name}")
                log_message(state, "ERROR", f"Tool Output: {result.stdout}")
                log_message(state, "ERROR", f"Tool Error: {result.stderr}")

        except Exception as e:
            log_message(state, "ERROR", f"Exception while converting {log_file.name}: {e}")

    log_message(state, "INFO", "Log conversion completed.")


def _move_files_from_device(state: UIState, source_subpath: str, dest_subpath: str) -> None:
    if not state.selected_device_serial:
        log_message(state, "ERROR", "No device selected.")
        return

    if not state.package_name:
        log_message(state, "ERROR", "Package Name not set.")
        return

    parts = state.package_name.split(".")
    if len(parts) < 3:
        log_message(state, "ERROR", "Invalid Package Name format. Cannot derive Project Name.")
        return
    project_name = parts[-1]

    # Source: /sdcard/Android/data/{package}/files/UnrealGame/{project}/{project}/Saved/{source_subpath}/
    # User confirmed structure: UnrealGame/{Name}/{Name}/Saved/...
    source_path = f"/sdcard/Android/data/{state.package_name}/files/UnrealGame/{project_name}/{project_name}/Saved/{source_subpath}/"
    
    # Dest: {state.output_path}/{dest_subpath}/
    dest_path = state.output_path / dest_subpath
    
    if not dest_path.exists():
        dest_path.mkdir(parents=True, exist_ok=True)

    client = AdbClient()
    serial = state.selected_device_serial

    log_message(state, "INFO", f"Moving files from {source_path} to {dest_path}...")

    try:
        # Pull all files from source directory
        # Append . to source path to pull contents
        client.pull(serial, source_path + ".", str(dest_path))
        
        # Delete files from source
        client.shell(serial, ["rm", "-rf", source_path + "*"])
        
        log_message(state, "SUCCESS", f"Moved files to {dest_path}")
    except AdbError as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "No such file or directory" in error_msg:
            file_type = "Logs" if "Logs" in dest_subpath else "CSV Data"
            log_message(state, "ERROR", f"No {file_type} present on device.")
        else:
            log_message(state, "ERROR", f"ADB Error: {e}")
    except Exception as e:
        log_message(state, "ERROR", f"Failed to move files: {e}")


def _render_log_entries(state: UIState) -> None:
    if not dpg.does_item_exist("log_container"):
        return

    dpg.delete_item("log_container", children_only=True)
    filter_value = state.log_filter.lower()
    filtered_logs = [
        entry
        for entry in state.logs
        if filter_value in entry[1].lower() or filter_value in entry[2].lower()
    ]

    if not filtered_logs:
        dpg.add_text(
            "No log entries match the filter.",
            color=(180, 180, 180),
            parent="log_container",
        )
        return

    for timestamp, level, message in filtered_logs:
        color = LOG_LEVEL_COLORS.get(level.upper(), (220, 220, 220))
        full_msg = f"[{timestamp}] [{level}] {message}"
        
        item = dpg.add_input_text(
            default_value=full_msg,
            readonly=True,
            width=-1,
            parent="log_container",
        )
        
        theme = _get_log_theme(level.upper(), color)
        dpg.bind_item_theme(item, theme)


_LOG_THEMES: dict[str, int] = {}


def _get_log_theme(level: str, color: tuple) -> int:
    if level in _LOG_THEMES:
        if dpg.does_item_exist(_LOG_THEMES[level]):
            return _LOG_THEMES[level]
            
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, color)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0, 0))
            
    _LOG_THEMES[level] = theme
    return theme


def log_message(state: UIState, level: str, message: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    state.logs.append((timestamp, level, message))
    _render_log_entries(state)


def _clear_logs(state: UIState) -> None:
    state.logs.clear()
    _render_log_entries(state)


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
            # Color code the Package Found column (last column)
            if column_index == len(values) - 1:  # Package Found column
                if device.package_found:
                    text_color = LOG_LEVEL_COLORS["SUCCESS"]  # Green
                else:
                    text_color = LOG_LEVEL_COLORS["ERROR"]  # Red
                # Use text with color instead of selectable for this column
                dpg.add_text(value, color=text_color, tag=cell_tag)
            else:
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
    
    # Check if package found on this device
    selected_device = None
    for device in state.devices:
        if device.serial == serial:
            selected_device = device
            break
            
    if selected_device and not selected_device.package_found:
        log_message(state, "WARNING", f"Package not found on {selected_device.make} {selected_device.model}. Please install the necessary package.")
        # Don't select the row
        return

    state.selected_device_serial = serial

    if not dpg.does_item_exist("device_table"):
        return
    _select_device_row(row_index, state)
    
    # Update output path if append is enabled
    if state.append_device_to_path:
        # Ensure base path is set
        if state.base_output_path is None:
            state.base_output_path = state.output_path

        # Find the device info
        selected_device = None
        for device in state.devices:
            if device.serial == serial:
                selected_device = device
                break
        
        if selected_device:
            device_folder = f"{selected_device.make}_{selected_device.model}"
            new_path = state.base_output_path / device_folder
            state.output_path = new_path
            if dpg.does_item_exist("output_path_label"):
                dpg.set_value("output_path_label", str(new_path))
            log_message(state, "INFO", f"Output path updated for new device: {new_path}")

    # Update output file name to match device make and model
    if selected_device:
        new_file_name = f"{selected_device.make}_{selected_device.model}"
        state.output_file_name = new_file_name
        if dpg.does_item_exist("output_file_name"):
            dpg.set_value("output_file_name", new_file_name)
        _auto_save_profile(state)


def _select_device_row(row_index: int, state: UIState) -> None:
    for index in range(len(state.devices)):
        dpg.unhighlight_table_row("device_table", index)

    dpg.highlight_table_row("device_table", row_index, SELECTED_ROW_COLOR)

    for cell_tags in state.device_cell_tags:
        for col_idx, tag in enumerate(cell_tags):
            # Skip the last column (Package Found) as it's a text widget, not selectable
            if col_idx < len(cell_tags) - 1 and dpg.does_item_exist(tag):
                dpg.set_value(tag, False)

    if 0 <= row_index < len(state.device_cell_tags):
        for col_idx, tag in enumerate(state.device_cell_tags[row_index]):
            # Skip the last column (Package Found) as it's a text widget, not selectable
            if col_idx < len(state.device_cell_tags[row_index]) - 1 and dpg.does_item_exist(tag):
                dpg.set_value(tag, True)


def _show_file_dialog(tag: str) -> None:
    if dpg.does_item_exist(tag):
        dpg.configure_item(tag, show=True)


def _register_file_dialogs(state: UIState) -> None:
    if not dpg.does_item_exist("input_path_dialog"):
        with dpg.file_dialog(
            directory_selector=True,  # Allow directory selection
            show=False,
            callback=_handle_input_path_selected,
            user_data=state,
            tag="input_path_dialog",
            width=600,
            height=400,
        ):
            dpg.add_file_extension(".csv", color=(0, 120, 255, 255))
            dpg.add_file_extension(".txt", color=(120, 255, 120, 255))
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
    # For directory selector, use file_path_name; for file selector, use selections
    selection = app_data.get("file_path_name") or next(iter(app_data.get("selections", {}).values()), None)
    if selection is None:
        return

    # Validate path exists before setting
    path = Path(selection)
    if not path.exists():
        return
    
    user_data.input_path = path
    if dpg.does_item_exist("input_path_label"):
        dpg.set_value("input_path_label", str(path))
        
    _auto_save_profile(user_data)


def _handle_output_path_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = app_data.get("file_path_name") or next(iter(app_data.get("selections", {}).values()), None)
    if selection is None:
        return

    new_base_path = Path(selection)
    user_data.base_output_path = new_base_path
    
    if user_data.append_device_to_path:
        # Re-apply device suffix
        selected_device = None
        if user_data.selected_device_serial:
            for device in user_data.devices:
                if device.serial == user_data.selected_device_serial:
                    selected_device = device
                    break
        
        if selected_device:
            device_folder = f"{selected_device.make}_{selected_device.model}"
            user_data.output_path = new_base_path / device_folder
        else:
             # Fallback if no device selected
             user_data.output_path = new_base_path
    else:
        user_data.output_path = new_base_path

    if dpg.does_item_exist("output_path_label"):
        dpg.set_value("output_path_label", str(user_data.output_path))
        
    _auto_save_profile(user_data)


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
             # Show warning and log it
             log_message(state, "WARNING", "Cannot edit Default Profile. Please create a New Profile or Open an existing one.")
             if not dpg.does_item_exist("default_profile_warning"):
                 with dpg.window(tag="default_profile_warning", label="Warning", modal=True, width=400, height=150):
                     dpg.add_text("Cannot edit the Default Profile.\nPlease create a New Profile or Open an existing one.")
                     dpg.add_button(label="OK", width=100, callback=lambda: dpg.delete_item("default_profile_warning"))
             return
    else:
        # Creating new profile
        log_message(state, "INFO", "Opening New Profile dialog")
        # Mark that we're creating a new profile
        state.is_creating_new_profile = True

    if dpg.does_item_exist("profile_dialog"):
        dpg.delete_item("profile_dialog")

    title = "Edit Profile" if is_edit else "New Profile"
    
    # Pre-fill values ONLY if editing an existing profile
    if is_edit:
        profile = state.profile_manager.current_profile
        nickname = profile.nickname if profile else ""
        package_name = state.package_name
    else:
        # For new profiles, start with empty values
        nickname = ""
        package_name = ""

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
            dpg.add_button(label="Save", callback=lambda: _handle_profile_save(state, is_edit))
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("profile_dialog"))
    
    # Register dialogs for this modal
    _register_profile_file_dialogs(state)


def _handle_profile_save(state: UIState, is_edit: bool) -> None:
    package_name = dpg.get_value("pd_package_name")
    nickname = dpg.get_value("pd_nickname")

    # Enhanced validation for package name format: com.{company}.{product}
    if not package_name:
        log_message(state, "ERROR", "Package Name cannot be empty.")
        return
    
    if not package_name.startswith("com."):
        log_message(state, "ERROR", f"Invalid Package Name: '{package_name}'. Package name must start with 'com.'")
        log_message(state, "INFO", "Correct format: com.{{company}}.{{product}} (e.g., com.lightfury.titan)")
        return
    
    # Check if it has at least 3 parts: com.company.product
    parts = package_name.split(".")
    if len(parts) < 3:
        log_message(state, "ERROR", f"Invalid Package Name: '{package_name}'. Must have format: com.{{company}}.{{product}}")
        log_message(state, "INFO", "Correct format: com.{{company}}.{{product}} (e.g., com.lightfury.titan)")
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
    
    # For NEW profiles, ALWAYS prompt for save location
    # For EDIT, only prompt if no path exists (shouldn't happen but safety check)
    if not is_edit or not state.profile_manager.current_profile_path:
        # This is a new profile - prompt for location
        # Store nickname for default filename
        state.temp_profile_nickname_for_save = nickname if nickname else "profile"
        _show_file_dialog("save_profile_as_dialog")
        # Store the temp values to save after path selection
        state.temp_profile_data = {
            "nickname": nickname,
            "package_name": package_name,
        }
    else:
        # Update existing profile
        profile = state.profile_manager.current_profile
        if profile:
            profile.nickname = nickname
            profile.package_name = package_name
            state.profile_manager.save_current_profile()
            state.profile_nickname = nickname or "None"
            
            log_message(state, "SUCCESS", f"Profile '{state.profile_nickname}' saved successfully.")

            # Refresh UI
            if dpg.does_item_exist("profile_nickname_input"):
                dpg.set_value("profile_nickname_input", state.profile_nickname)
            _update_profile_display_colors(state)
            pass


def _save_current_profile(state: UIState) -> None:
    if state.profile_manager.current_profile and state.profile_manager.current_profile_path:
        # Update profile from current UI state
        profile = state.profile_manager.current_profile
        profile.package_name = state.package_name
        
        # Update fields from UI/State
        if dpg.does_item_exist("output_file_name"):
            state.output_file_name = dpg.get_value("output_file_name")
        
        profile.output_file_name = state.output_file_name
        profile.input_path = str(state.input_path)
        
        # Save base_output_path if available to avoid saving the appended device path
        if state.base_output_path:
            profile.output_path = str(state.base_output_path)
        else:
            profile.output_path = str(state.output_path)
            
        profile.use_prefix_only = state.use_prefix_only
        profile.append_device_to_path = state.append_device_to_path
        
        state.profile_manager.save_current_profile()
    else:
        _show_file_dialog("save_profile_as_dialog")


def _auto_save_profile(state: UIState) -> None:
    """Automatically save specific fields to the current profile."""
    if state.profile_manager.current_profile and state.profile_manager.current_profile_path:
        profile = state.profile_manager.current_profile
        
        # Update fields
        if dpg.does_item_exist("output_file_name"):
            state.output_file_name = dpg.get_value("output_file_name")
            
        profile.output_file_name = state.output_file_name
        profile.input_path = str(state.input_path)
        
        # Save base_output_path if available to avoid saving the appended device path
        if state.base_output_path:
            profile.output_path = str(state.base_output_path)
        else:
            profile.output_path = str(state.output_path)
            
        profile.use_prefix_only = state.use_prefix_only
        profile.append_device_to_path = state.append_device_to_path
        
        state.profile_manager.save_current_profile()


def _register_profile_file_dialogs(state: UIState) -> None:
    if not dpg.does_item_exist("save_profile_as_dialog"):
        # Get default filename from temp nickname if available
        default_name = getattr(state, 'temp_profile_nickname_for_save', 'profile')
        default_filename = f"{default_name}.json" if default_name else "profile.json"
        
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=_handle_save_profile_as_selected,
            user_data=state,
            tag="save_profile_as_dialog",
            width=500,
            height=400,
            default_filename=default_filename,
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
    # Update state.output_file_name from UI
    if dpg.does_item_exist("output_file_name"):
        user_data.output_file_name = dpg.get_value("output_file_name")

    profile = user_data.profile_manager.create_new_profile(
        nickname=nickname,
        package_name=package_name,
        path=path
    )
    # Populate fields
    profile.output_file_name = user_data.output_file_name
    profile.input_path = str(user_data.input_path)
    profile.output_path = str(user_data.output_path)
    profile.use_prefix_only = user_data.use_prefix_only
    profile.append_device_to_path = user_data.append_device_to_path

    profile.save(path)
    
    log_message(user_data, "SUCCESS", f"New profile '{nickname}' created at {path}")

    # Update UI
    user_data.profile_nickname = nickname or "None"
    user_data.package_name = package_name
    user_data.profile_path = path
    
    if dpg.does_item_exist("profile_nickname_input"):
        dpg.set_value("profile_nickname_input", nickname or "None")
    if dpg.does_item_exist("profile_path_input"):
        dpg.set_value("profile_path_input", str(path))
        # _update_profile_path_display(path) # Removed as we use labels now
    if dpg.does_item_exist("package_input"):
        dpg.set_value("package_input", package_name)
    
    _update_profile_display_colors(user_data)


def _handle_open_profile_selected(sender: int, app_data: dict, user_data: UIState) -> None:
    selection = next(iter(app_data.get("selections", {}).values()), None)
    if selection:
        path = Path(selection)
        try:
            from cerebrus.core.profile import Profile
            profile = Profile.load(path)
            
            # Validate that required fields exist
            if not hasattr(profile, 'nickname') or not hasattr(profile, 'package_name'):
                raise ValueError("Profile missing required fields")
            
            user_data.profile_manager.current_profile = profile
            user_data.profile_manager.current_profile_path = path
            user_data.profile_manager.set_last_used_profile_path(path)
            
            log_message(user_data, "SUCCESS", f"Profile loaded: {profile.nickname} from {path}")

            # Update UI
            user_data.profile_nickname = profile.nickname or "None"
            user_data.package_name = profile.package_name
            user_data.profile_path = path
            
            # Load persisted fields
            user_data.output_file_name = profile.output_file_name
            user_data.input_path = Path(profile.input_path) if profile.input_path else Path("")
            user_data.output_path = Path(profile.output_path) if profile.output_path else Path("")
            user_data.use_prefix_only = profile.use_prefix_only
            user_data.append_device_to_path = profile.append_device_to_path
            
            # Update UI elements
            if dpg.does_item_exist("package_input"):
                dpg.set_value("package_input", profile.package_name)
            
            if dpg.does_item_exist("profile_nickname_input"):
                dpg.set_value("profile_nickname_input", profile.nickname or "None")
            
            if dpg.does_item_exist("profile_path_input"):
                dpg.set_value("profile_path_input", str(path))
                
            if dpg.does_item_exist("output_file_name"):
                dpg.set_value("output_file_name", user_data.output_file_name)
                
            if dpg.does_item_exist("input_path_label"):
                dpg.set_value("input_path_label", str(user_data.input_path))
                
            if dpg.does_item_exist("output_path_label"):
                dpg.set_value("output_path_label", str(user_data.output_path))
                
            if dpg.does_item_exist("use_prefix_only"):
                dpg.set_value("use_prefix_only", user_data.use_prefix_only)
                
            if dpg.does_item_exist("append_device_to_path"):
                dpg.set_value("append_device_to_path", user_data.append_device_to_path)
            
            _update_profile_display_colors(user_data)
            
        except (ValueError, KeyError, TypeError) as e:
            # Invalid profile schema
            filename = path.name if path else "Unknown"
            log_message(user_data, "ERROR", f"{filename} is not a valid Profile. Please create a new profile or open a valid existing profile.")
            print(f"Error loading profile: {e}")
        except Exception as e:
            # Other errors (file not found, JSON parse error, etc.)
            filename = path.name if path else "Unknown"
            log_message(user_data, "ERROR", f"Failed to load {filename}: {str(e)}")
            print(f"Error loading profile: {e}")


def _update_profile_display_colors(state: UIState) -> None:
    """Update the display colors for profile labels based on whether it's default or loaded."""
    profile_color = (255, 210, 120) if not state.profile_manager.current_profile_path else (150, 255, 150)
    
    if dpg.does_item_exist("profile_nickname_input"):
        dpg.configure_item("profile_nickname_input", color=profile_color)
    if dpg.does_item_exist("profile_path_input"):
        dpg.configure_item("profile_path_input", color=profile_color)
    if dpg.does_item_exist("package_input"):
        dpg.configure_item("package_input", color=profile_color)


def _update_profile_path_display(path: Path) -> None:
    # Deprecated/Unused for labels but kept if needed or just remove?
    # User said "Should auto adjust the size for the complete path to be visible."
    # Labels auto-adjust.
    pass


def _add_help_button(tooltip_key: str) -> None:
    """Add a small '?' help button with tooltip."""
    tooltip_text = TOOLTIPS.get(tooltip_key, "No help available.")
    button = dpg.add_button(label="?", width=20, height=20, callback=lambda: None)
    
    with dpg.tooltip(button):
        # Wrap text to max width for readability
        dpg.add_text(tooltip_text, wrap=400)

