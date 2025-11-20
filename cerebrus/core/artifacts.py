"""Helpers for locating and retrieving Unreal artifacts from Android devices."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cerebrus.config.models import ProjectDefinition, ProjectStream
from cerebrus.core.logging import get_logger
from cerebrus.core.projects import ProjectRegistry
from cerebrus.core.state import Device
from cerebrus.tools.uaft import UAFTTool

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class DeviceArtifactListing:
    """Container for log/profile files discovered on a device."""

    logs: list[Path]
    profiles: list[Path]

    def filtered(self, keyword: str) -> "DeviceArtifactListing":
        if not keyword:
            return self
        lowered = keyword.lower()
        return DeviceArtifactListing(
            logs=[item for item in self.logs if lowered in item.name.lower()],
            profiles=[item for item in self.profiles if lowered in item.name.lower()],
        )


@dataclass(slots=True)
class AndroidArtifactManager:
    """Coordinate UAFT/ADB interactions for pulling Unreal artifacts."""

    uaft: UAFTTool
    project_registry: ProjectRegistry
    cache_root: Path

    def list_artifacts(
        self, device: Device, project: ProjectDefinition, stream: ProjectStream | None = None
    ) -> DeviceArtifactListing:
        log_dir = project.device_log_path(stream)
        profile_dir = project.device_profile_path(stream)
        LOGGER.info("Listing device artifacts from %s", log_dir)
        logs = self.uaft.list_remote_files(device, log_dir)
        profiles = self.uaft.list_remote_files(device, profile_dir)
        return DeviceArtifactListing(logs=logs, profiles=profiles)

    def pull_selected(
        self,
        device: Device,
        project: ProjectDefinition,
        listing: DeviceArtifactListing,
        *,
        logs: list[Path] | None = None,
        profiles: list[Path] | None = None,
    ) -> list[Path]:
        """Download the selected artifacts into the cache directory."""

        destination = self._destination_for(project)
        downloaded: list[Path] = []

        if logs:
            downloaded.extend(
                self.uaft.pull_files(
                    device,
                    project.device_log_path(),
                    destination,
                    files=logs,
                )
            )
        if profiles:
            downloaded.extend(
                self.uaft.pull_files(
                    device,
                    project.device_profile_path(),
                    destination,
                    files=profiles,
                )
            )

        if not logs and not profiles:
            LOGGER.info("No specific selection provided; pulling entire directories")
            downloaded.extend(
                self.uaft.pull_files(device, project.device_log_path(), destination, files=None)
            )
            downloaded.extend(
                self.uaft.pull_files(device, project.device_profile_path(), destination, files=None)
            )

        return downloaded

    def _destination_for(self, project: ProjectDefinition) -> Path:
        root = self.cache_root / "device_captures" / project.project
        root.mkdir(parents=True, exist_ok=True)
        return root


__all__ = ["AndroidArtifactManager", "DeviceArtifactListing"]
