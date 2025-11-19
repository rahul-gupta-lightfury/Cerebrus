"""Dear PyGui dashboard scaffold used by ``python -m cerebrus``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:  # pragma: no cover - Dear PyGui is optional during tests
    import dearpygui.dearpygui as dpg
except Exception:  # noqa: BLE001 - environments without a GPU/display fall back to logs
    dpg = None

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
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

    def __post_init__(self) -> None:
        self.device_panel = DevicePanel(device_manager=self.device_manager)
        self.capture_panel = CapturePanel(state=self.state)
        self.report_panel = ReportPanel(state=self.state)
        self.config_panel = ConfigPanel(state=self.state)
        self._log_widget_tag = "cerebrus-live-log"

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
        width, height = 1700, 980
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
        dpg.add_text(
            "Cerebrus: Real-time Profiling Toolkit",
            color=(173, 216, 230, 255),
            bullet=False,
        )
        dpg.add_text(
            "Python Dear PyGui scaffold that mirrors the reference screenshot layout",
            color=(200, 200, 200, 255),
        )
        dpg.add_separator()

        sections = self._build_layout_sections()
        midpoint = len(sections) // 2
        left, right = sections[:midpoint], sections[midpoint:]

        with dpg.group(horizontal=True):
            self._render_section_column(left, width=800)
            self._render_section_column(right, width=800)

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
