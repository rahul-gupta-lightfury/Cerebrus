"""Dear PyGui dashboard scaffold used by ``python -m cerebrus``."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

try:  # pragma: no cover - Dear PyGui is optional during tests
    import dearpygui.dearpygui as dpg
except Exception:  # noqa: BLE001 - environments without a GPU/display fall back to logs
    dpg = None

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
from cerebrus.core.artifacts import AndroidArtifactManager
from cerebrus.ui.capture_panel import CapturePanel
from cerebrus.ui.config_panel import ConfigPanel
from cerebrus.ui.device_panel import DevicePanel
from cerebrus.ui.report_panel import ReportPanel

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class UILayoutSection:
    """Represents a conceptual block from the design reference."""

    title: str
    rows: list[str]

    def render(self) -> str:
        lines = [self.title, "-" * len(self.title)]
        lines.extend(f"  • {row}" for row in self.rows)
        return "\n".join(lines)


@dataclass
class CerebrusUI:
    """Aggregates the individual Dear PyGui panels."""

    state: ApplicationState
    device_manager: DeviceManager
    artifact_manager: AndroidArtifactManager

    def __post_init__(self) -> None:
        self.device_panel = DevicePanel(device_manager=self.device_manager)
        self.capture_panel = CapturePanel(
            state=self.state, artifact_manager=self.artifact_manager
        )
        self.report_panel = ReportPanel(state=self.state)
        self.config_panel = ConfigPanel(state=self.state)
        self._log_widget_tag = "cerebrus-live-log"
        self._viewport_size: tuple[int, int] = (1700, 980)
        self._output_dir_field = "cerebrus-output-dir"
        self._output_name_field = "cerebrus-output-name"
        self._output_dialog_tag = "cerebrus-output-dialog"

    def render_once(self) -> None:
        LOGGER.info("Rendering UI scaffold")
        self.device_panel.render()
        self.capture_panel.render()
        self.report_panel.render()
        self.config_panel.render()

        for section in self._build_layout_sections():
            LOGGER.info("\n%s", section.render())

    def run(self) -> None:
        """Launch the Dear PyGui dashboard or fall back to the log-based layout."""

        if dpg is None:
            LOGGER.warning(
                "Dear PyGui is unavailable. Falling back to console-rendered layout."
            )
            self.render_once()
            return

        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True)
        self._build_viewport()
        # Activate before setup/show to avoid a docking-only viewport and repeat after show
        # because some Dear PyGui versions reset the primary window on first display.
        self._activate_primary_window()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self._activate_primary_window()

        try:
            while dpg.is_dearpygui_running():
                self._refresh_live_log()
                dpg.render_dearpygui_frame()
        finally:  # pragma: no cover - Dear PyGui teardown is GUI-driven
            dpg.destroy_context()

    def _build_layout_sections(self) -> list[UILayoutSection]:
        """Return pseudo-layout data that mirrors the provided screenshot."""

        return [
            UILayoutSection(
                title="Project + Session Overview",
                rows=[
                    f"Active project: {self.state.active_project.project if self.state.active_project else 'Not set'}",
                    f"Cache: {self.state.cache_directory.resolve()}",
                    "Goal: Launch-to-insights bridge for Android perf workflows",
                    "Status blocks match the shared reference screenshot",
                ],
            ),
            UILayoutSection(
                title="Connected Devices",
                rows=list(self._device_rows())
                or ["No Android devices detected via UAFT"],
            ),
            UILayoutSection(
                title="Capture Session & Descriptor Details",
                rows=[
                    "Session Descriptor: Device | Build ID | Performance Target | Notes",
                    "CSV filters and stat sets will be defined per run",
                    "Actions: Capture Session, Stream Logs, Pull CSV",
                    "Dear PyGui widgets mirror the original capture controls",
                ],
            ),
            UILayoutSection(
                title="Reports, Environment & Health",
                rows=[
                    "PerfReportTool summary + CSV convert/filter helpers",
                    "Env health: tool paths, cache size, last sync, log state",
                    "Insights streaming prepares CSV/Insights pairs",
                    "Command buttons: Generate Report | Mark Session Complete",
                ],
            ),
        ]

    def _device_rows(self) -> Iterable[str]:
        for device in self.state.devices:
            yield f"{device.model} ({device.identifier}) — Android {device.android_version}"

    # Dear PyGui helpers -------------------------------------------------

    def _build_viewport(self) -> None:
        width, height = self._compute_viewport_size()
        self._viewport_size = (width, height)
        dpg.create_viewport(title="Cerebrus Toolkit Dashboard", width=width, height=height)
        with dpg.window(
            tag="cerebrus_root",
            label="Cerebrus Toolkit",
            width=width - 40,
            height=height - 60,
            no_move=True,
            no_resize=True,
        ):
            self._render_dashboard_body()

    def _activate_primary_window(self) -> None:
        """Ensure the root window becomes the active Dear PyGui viewport."""

        if not dpg.does_item_exist("cerebrus_root"):
            LOGGER.warning("Primary window tag missing; skipping activation")
            return
        dpg.set_primary_window("cerebrus_root", True)

    def _render_performance_controls(self) -> None:
        """Render performance action controls with output path inputs."""

        with dpg.group(horizontal=True):
            dpg.add_button(label="Performance", callback=self._log_performance_trigger)
            dpg.add_input_text(
                tag=self._output_dir_field,
                label="Output Directory",
                default_value=str(self.state.output_directory or ""),
                width=320,
                readonly=True,
            )
            dpg.add_button(label="Browse Output Directory", callback=self._open_output_dialog)
            dpg.add_input_text(
                tag=self._output_name_field,
                label="Output Name",
                default_value=self.state.output_name,
                width=200,
            )

        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            callback=self._set_output_directory,
            tag=self._output_dialog_tag,
        ):
            dpg.add_file_extension("")

    def _render_dashboard_body(self) -> None:
        self._render_menu_bar()
        dpg.add_spacer(height=6)

        dpg.add_text(
            "Cerebrus: Real-time Profiling Toolkit",
            color=(173, 216, 230, 255),
            bullet=False,
        )
        dpg.add_text(
            "Python Dear PyGui scaffold that mirrors the reference screenshot layout",
            color=(200, 200, 200, 255),
        )
        dpg.add_text(
            f"Active project: {self.state.active_project.project if self.state.active_project else 'Not set'}",
            color=(160, 220, 255, 255),
            bullet=True,
        )
        dpg.add_text(
            f"Cache Path: {self.state.cache_directory.resolve()}",
            color=(160, 220, 255, 255),
            bullet=True,
        )
        self._render_performance_controls()
        dpg.add_separator()

        sections = self._build_layout_sections()
        midpoint = len(sections) // 2
        left, right = sections[:midpoint], sections[midpoint:]

        with dpg.group(horizontal=True):
            left_width, right_width = self._column_widths()
            self._render_section_column(left, width=left_width)
            self._render_section_column(right, width=right_width)

        dpg.add_separator()
        self._render_log_console()

    def _render_section_column(self, sections: list[UILayoutSection], width: int) -> None:
        for section in sections:
            height = 110 + len(section.rows) * 26
            with dpg.child_window(width=width, height=height, border=True):
                dpg.add_text(section.title, color=(255, 215, 0, 255))
                dpg.add_separator()
                for row in section.rows:
                    dpg.add_text(row, wrap=width - 20)
            dpg.add_spacer(height=8)

    def _render_log_console(self) -> None:
        dpg.add_text("Session Live Log", color=(144, 238, 144, 255))
        with dpg.child_window(height=220, border=True):
            dpg.add_text(
                "Streaming log output updates in real time (refresh ~30 FPS)",
                color=(180, 180, 180, 255),
            )
            self._log_widget_tag = "cerebrus-live-log"
            dpg.add_input_text(
                tag=self._log_widget_tag,
                multiline=True,
                readonly=True,
                default_value=self._log_contents(),
                width=-1,
                height=160,
            )

    def _open_output_dialog(self) -> None:
        dpg.show_item(self._output_dialog_tag)

    def _set_output_directory(self, sender: int, app_data: dict[str, str]) -> None:
        selected = app_data.get("file_path_name")
        if not selected:
            return
        self.state.output_directory = Path(selected)
        dpg.set_value(self._output_dir_field, str(self.state.output_directory))
        LOGGER.info("Output directory set to %s", self.state.output_directory)

    def _log_performance_trigger(self) -> None:
        self.state.output_name = dpg.get_value(self._output_name_field)
        LOGGER.info(
            "Performance action requested (dir=%s, name=%s)",
            self.state.output_directory,
            self.state.output_name,
        )

    def _refresh_live_log(self) -> None:
        if not dpg.does_item_exist(self._log_widget_tag):
            return
        dpg.set_value(self._log_widget_tag, self._log_contents())

    def _log_contents(self) -> str:
        if not self.state.log_buffer:
            return "Live log buffer not initialized"
        return self.state.log_buffer.joined() or "(Log output will appear here)"

    # Menu helpers -------------------------------------------------------

    def _render_menu_bar(self) -> None:
        with dpg.menu_bar():
            self._menu_with_items(
                "File",
                [
                    ("New", None),
                    ("Open", None),
                ],
            )
            self._menu_with_items(
                "View",
                [
                    ("Reset Layout", None),
                    ("Toggle Docking", self._toggle_docking),
                ],
            )
            self._menu_with_items(
                "Tools",
                [
                    ("Echo Test Command", self._log_tool_echo),
                    ("Refresh Devices", self._refresh_devices),
                ],
            )
            self._menu_with_items(
                "Settings",
                [
                    ("Load Theme...", None),
                    ("Log Colors", None),
                    ("Key Bindings", None),
                ],
            )
            self._menu_with_items(
                "Help",
                [
                    ("Help", None),
                    ("Provide Feedback", None),
                    ("About", self._log_about),
                ],
            )

    def _menu_with_items(self, label: str, entries: list[tuple[str, Callable | None]]) -> None:
        with dpg.menu(label=label):
            for entry_label, callback in entries:
                dpg.add_menu_item(label=entry_label, callback=callback, enabled=callback is not None)

    def _log_tool_echo(self) -> None:
        LOGGER.info("Echo test command placeholder")

    def _refresh_devices(self) -> None:
        refreshed = self.device_manager.refresh()
        self.state.set_devices(refreshed)
        LOGGER.info("Device list refreshed (%d device(s))", len(refreshed))

    def _toggle_docking(self) -> None:
        try:
            current = dpg.get_app_configuration().get("docking")
        except Exception:
            current = True
        dpg.configure_app(docking=not bool(current), docking_space=True)
        LOGGER.info("Docking toggled to %s", not bool(current))

    def _log_about(self) -> None:
        LOGGER.info("Cerebrus Dear PyGui scaffold — version preview")

    # Layout utilities ---------------------------------------------------

    def _compute_viewport_size(self) -> tuple[int, int]:
        """Clamp the viewport to the monitor resolution to avoid overflow."""

        desired_width, desired_height = 1700, 980
        try:
            monitor = dpg.get_primary_monitor()
        except Exception:  # pragma: no cover - depends on Dear PyGui environment
            monitor = None

        if not monitor:
            return desired_width, desired_height

        work_size = monitor.get("work_size") or monitor.get("size")
        if not work_size:
            return desired_width, desired_height

        max_width, max_height = work_size
        padding_width, padding_height = 40, 80
        width = min(desired_width, max_width - padding_width)
        height = min(desired_height, max_height - padding_height)
        return max(width, 640), max(height, 480)

    def _column_widths(self) -> tuple[int, int]:
        total_available = max(self._viewport_size[0] - 80, 640)
        column_width = max(total_available // 2, 320)
        return column_width, column_width
