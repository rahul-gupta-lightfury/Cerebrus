"""Registry for per-project Unreal directory conventions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from cerebrus.config import ProjectDefinition, ProjectStore
from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ProjectRegistry:
    """Cache project definitions and expose helper lookups."""

    store: ProjectStore
    cache_directory: Path
    _projects: list[ProjectDefinition] = field(default_factory=list)
    _active_key: str | None = None

    def __post_init__(self) -> None:
        self.cache_directory.mkdir(parents=True, exist_ok=True)
        if self.store.cache_file is None:
            self.store.cache_file = self.cache_directory / "projects.json"
        self.reload()

    def reload(self) -> None:
        self._projects = self.store.load()
        if self._projects and not self._active_key:
            self._active_key = self._projects[0].key
        LOGGER.debug("Project registry initialized with %d projects", len(self._projects))

    def list_projects(self) -> list[ProjectDefinition]:
        return list(self._projects)

    def active_project(self) -> ProjectDefinition | None:
        return next((p for p in self._projects if p.key == self._active_key), None)

    def set_active(self, key: str) -> None:
        if not any(p.key == key for p in self._projects):
            raise KeyError(f"Unknown project key: {key}")
        self._active_key = key
        LOGGER.info("Active project set to %s", key)

    def remember_paths(
        self, project: ProjectDefinition, *, device_root: Path | None, pc_root: Path | None
    ) -> None:
        self.store.remember_paths(project, device_root=device_root, pc_root=pc_root)
        self.reload()

    def inject_projects(self, definitions: Iterable[ProjectDefinition]) -> None:
        """Used by tests to seed the registry without hitting disk."""

        self._projects = list(definitions)
        self._active_key = self._projects[0].key if self._projects else None


__all__ = ["ProjectRegistry"]
