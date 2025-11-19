"""Tests for the Dear PyGui layout scaffolding."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from cerebrus.config.models import CacheConfig, CerebrusConfig, ProjectProfile, ToolPaths
from cerebrus.core.state import ApplicationState, Device
from cerebrus.ui.main_window import CerebrusUI


class _StubDeviceManager:
    def __init__(self, devices: Iterable[Device]):
        self._devices = list(devices)

    def get_connected(self) -> list[Device]:
        return list(self._devices)


def _build_state(devices: Iterable[Device]) -> ApplicationState:
    config = CerebrusConfig(
        tool_paths=ToolPaths(),
        profiles=[ProjectProfile(name="default", report_type="summary")],
        cache=CacheConfig(directory=Path(".cache")),
    )
    state = ApplicationState(config=config)
    state.set_devices(devices)
    state.active_profile = config.profiles[0]
    return state


def test_layout_sections_match_reference_language() -> None:
    devices = [Device(identifier="FAKE123", model="Pixel 8", android_version="14")]
    state = _build_state(devices)
    ui = CerebrusUI(state=state, device_manager=_StubDeviceManager(devices))

    sections = ui._build_layout_sections()
    titles = [section.title for section in sections]

    assert "Project + Session Overview" in titles
    assert any("Launch-to-insights bridge" in row for row in sections[0].rows)
    assert any("Session Descriptor" in row for row in sections[2].rows)


def test_log_contents_uses_live_buffer() -> None:
    state = _build_state([])
    state.log_buffer.append("boot complete")
    ui = CerebrusUI(state=state, device_manager=_StubDeviceManager([]))

    assert "boot complete" in ui._log_contents()
