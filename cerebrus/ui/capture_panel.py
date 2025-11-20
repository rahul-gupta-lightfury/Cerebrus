"""Capture panel stub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from cerebrus.core.artifacts import AndroidArtifactManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState, Device

LOGGER = get_logger(__name__)


@dataclass
class CapturePanel:
    state: ApplicationState
    artifact_manager: AndroidArtifactManager

    def render(self) -> None:
        project = self.state.active_project
        device = self._selected_device()
        if not project or not device:
            LOGGER.info("Capture panel awaiting project selection and connected device")
            return

        stream = self.state.active_stream
        listing = self.artifact_manager.list_artifacts(device, project, stream=stream)
        filtered = listing.filtered(self.state.capture_filter)

        LOGGER.info(
            "Capture panel (%s/%s): %d logs, %d CSV profiles",
            project.company,
            project.project,
            len(filtered.logs),
            len(filtered.profiles),
        )
        if self.state.capture_filter:
            LOGGER.info("Filter applied: %s", self.state.capture_filter)
        if filtered.logs:
            LOGGER.info("Log files: %s", ", ".join(path.name for path in filtered.logs))
        if filtered.profiles:
            LOGGER.info("Profiling CSVs: %s", ", ".join(path.name for path in filtered.profiles))

    def pull_all(self) -> list[str]:
        """Download every log and profile for the active project/device."""

        project = self.state.active_project
        device = self._selected_device()
        if not project or not device:
            LOGGER.info("Cannot pull artifacts without a project and device")
            return []

        listing = self.artifact_manager.list_artifacts(device, project, stream=self.state.active_stream)
        downloaded = self.artifact_manager.pull_selected(device, project, listing)
        return [str(path) for path in downloaded]

    def pull_selected(self, logs: Iterable[str], profiles: Iterable[str]) -> list[str]:
        """Download specific files selected by the user."""

        project = self.state.active_project
        device = self._selected_device()
        if not project or not device:
            LOGGER.info("Cannot pull artifacts without a project and device")
            return []

        listing = self.artifact_manager.list_artifacts(device, project, stream=self.state.active_stream)
        log_paths = [path for path in listing.logs if path.name in set(logs)]
        profile_paths = [path for path in listing.profiles if path.name in set(profiles)]
        downloaded = self.artifact_manager.pull_selected(
            device, project, listing, logs=log_paths, profiles=profile_paths
        )
        return [str(path) for path in downloaded]

    def _selected_device(self) -> Device | None:
        if not self.state.devices:
            return None
        return self.state.devices[0]
