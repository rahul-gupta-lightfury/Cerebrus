"""Device panel stub."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass
class DevicePanel:
    device_manager: DeviceManager

    def render(self) -> None:
        devices = self.device_manager.get_connected()
        LOGGER.info("Device panel rendering %d devices", len(devices))
