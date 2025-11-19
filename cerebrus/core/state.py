"""State models shared across the Cerebrus core layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from cerebrus.config.models import CerebrusConfig, ProjectProfile
from cerebrus.core.log_buffer import LiveLogBuffer


@dataclass(slots=True)
class Device:
    """Represents an Android target device."""

    identifier: str
    model: str
    android_version: str


@dataclass(slots=True)
class ApplicationState:
    """In-memory representation of the running application."""

    config: CerebrusConfig
    devices: list[Device] = field(default_factory=list)
    active_profile: ProjectProfile | None = None
    log_buffer: LiveLogBuffer = field(default_factory=LiveLogBuffer)

    def set_devices(self, devices: Iterable[Device]) -> None:
        self.devices = list(devices)

    @property
    def cache_directory(self) -> Path:
        return self.config.cache.directory
