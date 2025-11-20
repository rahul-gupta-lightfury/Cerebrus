from __future__ import annotations

from pathlib import Path

from cerebrus.config.models import ProjectDefinition, ProjectStream
from cerebrus.config.project_store import ProjectStore
from cerebrus.core.artifacts import AndroidArtifactManager
from cerebrus.core.projects import ProjectRegistry
from cerebrus.core.state import Device
from cerebrus.tools.uaft import UAFTTool


def _project(tmp_path: Path) -> ProjectDefinition:
    return ProjectDefinition(
        company="ACME",
        project="RocketGame",
        package="com.acme.rocket",
        device_root=Path("/sdcard/Android/data/com.acme.rocket/files"),
        pc_root=tmp_path,
        streams=[ProjectStream(name="default", device_subdir="Saved/Logs")],
    )


def test_artifact_manager_lists_and_pulls(tmp_path: Path) -> None:
    project = _project(tmp_path)
    store = ProjectStore(definition_file=tmp_path / "base.json")
    registry = ProjectRegistry(store=store, cache_directory=tmp_path)
    registry.inject_projects([project])
    manager = AndroidArtifactManager(
        uaft=UAFTTool(binary=None), project_registry=registry, cache_root=tmp_path
    )

    device = Device(identifier="FAKE123", model="Pixel", android_version="14")
    listing = manager.list_artifacts(device, project)

    assert listing.logs

    pulled = manager.pull_selected(device, project, listing, logs=listing.logs, profiles=[])
    assert all(path.exists() for path in pulled)
