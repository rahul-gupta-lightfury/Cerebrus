"""State models shared across the Cerebrus core layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import json

from cerebrus.config.models import (
    CerebrusConfig,
    ProjectDefinition,
    ProjectProfile,
    ProjectStream,
)
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
    projects: list[ProjectDefinition] = field(default_factory=list)
    active_project: ProjectDefinition | None = None
    active_stream: ProjectStream | None = None
    capture_filter: str = ""
    log_buffer: LiveLogBuffer = field(default_factory=LiveLogBuffer)
    profile_storage_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.profile_storage_path = self.cache_directory / "profiles.json"

    def set_devices(self, devices: Iterable[Device]) -> None:
        self.devices = list(devices)

    def set_projects(self, projects: Iterable[ProjectDefinition]) -> None:
        self.projects = list(projects)
        self.active_project = self.projects[0] if self.projects else None
        if self.active_project and self.active_project.streams:
            self.active_stream = self.active_project.streams[0]

    @property
    def cache_directory(self) -> Path:
        return self.config.cache.directory

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
