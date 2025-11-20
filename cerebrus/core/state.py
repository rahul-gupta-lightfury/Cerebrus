"""State models shared across the Cerebrus core layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import json

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
    active_device_id: str | None = None
    log_buffer: LiveLogBuffer = field(default_factory=LiveLogBuffer)
    profile_storage_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.profile_storage_path = self.cache_directory / "profiles.json"

    def set_devices(self, devices: Iterable[Device]) -> None:
        self.devices = list(devices)
        identifiers = {device.identifier for device in self.devices}
        if self.active_device_id not in identifiers:
            self.active_device_id = next(iter(identifiers), None)

    @property
    def cache_directory(self) -> Path:
        return self.config.cache.directory

    @property
    def active_device(self) -> Device | None:
        for device in self.devices:
            if device.identifier == self.active_device_id:
                return device
        return None

    def set_active_device(self, device_id: str | None) -> None:
        """Persist the selected device identifier for downstream use."""

        self.active_device_id = device_id

    def save_profiles_to_json(self) -> Path:
        """Persist configured profiles to JSON for downstream caching paths."""

        profiles_blob = [
            {
                "name": profile.name,
                "report_type": profile.report_type,
                "csv_filters": list(profile.csv_filters),
                "description": profile.description,
            }
            for profile in self.config.profiles
        ]
        payload = {
            "active_profile": self.active_profile.name if self.active_profile else None,
            "profiles": profiles_blob,
        }
        self.profile_storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.profile_storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.profile_storage_path
