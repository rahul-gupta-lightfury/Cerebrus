"""Device management layer for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from cerebrus.core.logging import get_logger
from cerebrus.core.state import Device
from cerebrus.tools.uaft import UAFTTool

LOGGER = get_logger(__name__)


@dataclass
class DeviceManager:
    """High-level orchestration around UAFT-based device discovery."""

    uaft: UAFTTool
    _devices: list[Device] = field(default_factory=list)

    def refresh(self) -> list[Device]:
        """Refresh the device list using UAFT and return the snapshot."""
        LOGGER.info("Refreshing connected devices via UAFT")
        self._devices = self.uaft.list_devices()
        return list(self._devices)

    def get_connected(self) -> list[Device]:
        """Return the cached device list."""
        return list(self._devices)

    def select_first_available(self) -> Device | None:
        """Return the first connected device, if available."""
        return self._devices[0] if self._devices else None

    def apply_snapshot(self, devices: Iterable[Device]) -> None:
        """Inject an externally-provided snapshot (useful for tests)."""
        self._devices = list(devices)
