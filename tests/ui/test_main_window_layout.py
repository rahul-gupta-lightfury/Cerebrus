"""Tests for the Dear PyGui layout scaffolding."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pytest

from cerebrus.config.models import CacheConfig, CerebrusConfig, ProjectProfile, ToolPaths
from cerebrus.core.state import ApplicationState, Device
from cerebrus.ui.main_window import CerebrusUI


class _StubDeviceManager:
    def __init__(self, devices: Iterable[Device]):
        self._devices = list(devices)

    def get_connected(self) -> list[Device]:
        return list(self._devices)


class _StubArtifactManager:
    class _StubListing:
        logs: list[str] = []
        profiles: list[str] = []

        def filtered(self, *_):
            return self

    def list_artifacts(self, *_, **__):  # pragma: no cover - logging only
        return self._StubListing()


def _build_state(devices: Iterable[Device]) -> ApplicationState:
    config = CerebrusConfig(
        tool_paths=ToolPaths(),
        cache=CacheConfig(directory=Path(".cache")),
    )
    state = ApplicationState(config=config)
    state.set_devices(devices)
    return state


def test_layout_sections_match_reference_language() -> None:
    devices = [Device(identifier="FAKE123", model="Pixel 8", android_version="14")]
    state = _build_state(devices)
    ui = CerebrusUI(
        state=state,
        device_manager=_StubDeviceManager(devices),
        artifact_manager=_StubArtifactManager(),
    )

    sections = ui._build_layout_sections()
    titles = [section.title for section in sections]

    assert "Project + Session Overview" in titles
    assert any("Launch-to-insights bridge" in row for row in sections[0].rows)
    assert any("Session Descriptor" in row for row in sections[2].rows)


def test_log_contents_uses_live_buffer() -> None:
    state = _build_state([])
    state.log_buffer.append("boot complete")
    ui = CerebrusUI(
        state=state,
        device_manager=_StubDeviceManager([]),
        artifact_manager=_StubArtifactManager(),
    )

    assert "boot complete" in ui._log_contents()


@pytest.mark.parametrize("exists", [True, False])
def test_primary_window_activation_guard(monkeypatch: pytest.MonkeyPatch, exists: bool) -> None:
    state = _build_state([])
    ui = CerebrusUI(
        state=state,
        device_manager=_StubDeviceManager([]),
        artifact_manager=_StubArtifactManager(),
    )

    recorded: list[str] = []

    class _StubDPG:
        @staticmethod
        def does_item_exist(tag: str) -> bool:  # pragma: no cover - trivial
            return exists and tag == "cerebrus_root"

        @staticmethod
        def set_primary_window(tag: str, value: bool) -> None:  # pragma: no cover - trivial
            recorded.append(f"{tag}={value}")

    monkeypatch.setattr("cerebrus.ui.main_window.dpg", _StubDPG())

    ui._activate_primary_window()

    if exists:
        assert recorded == ["cerebrus_root=True"]
    else:
        assert recorded == []
