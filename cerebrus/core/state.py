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
    output_directory: Path | None = None
    output_name: str = ""

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

