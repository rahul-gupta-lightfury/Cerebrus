"""Dear PyGui dashboard scaffold used by ``python -m cerebrus``."""

from __future__ import annotations

from dataclasses import dataclass
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
        dpg.setup_dearpygui()
        dpg.show_viewport()

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
                    f"Active profile: {self._active_profile_name()}",
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
                    "CSV filters and stat sets derive from the active profile",
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

    def _active_profile_name(self) -> str:
        return self.state.active_profile.name if self.state.active_profile else "default"

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
        dpg.set_primary_window("cerebrus_root", True)

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
            f"Profile: {self._active_profile_name()}",
            color=(160, 220, 255, 255),
            bullet=True,
        )
        dpg.add_text(
            f"Profile Path: {self.state.profile_storage_path}",
            color=(160, 220, 255, 255),
            bullet=True,
        )
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
                    ("Save Profiles", self._handle_save_profiles),
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
            self._render_profile_menu()
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

    def _render_profile_menu(self) -> None:
        with dpg.menu(label="Profile"):
            dpg.add_menu_item(label=f"Active: {self._active_profile_name()}", enabled=False)
            dpg.add_menu_item(label=f"Path: {self.state.profile_storage_path}", enabled=False)
            dpg.add_separator()
            for profile in self.state.config.profiles:
                dpg.add_menu_item(
                    label=profile.name,
                    callback=lambda _, p=profile: self._set_active_profile(p),
                )
            dpg.add_separator()
            dpg.add_menu_item(label="Save Profiles", callback=self._handle_save_profiles)

    def _set_active_profile(self, profile: object) -> None:
        try:
            profile_name = profile.name  # type: ignore[attr-defined]
        except Exception:
            LOGGER.warning("Invalid profile selection: %s", profile)
            return
        self.state.active_profile = profile  # type: ignore[assignment]
        LOGGER.info("Active profile set to %s", profile_name)

    def _handle_save_profiles(self) -> None:
        saved_path = self.state.save_profiles_to_json()
        LOGGER.info("Profiles saved to %s", saved_path)

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
