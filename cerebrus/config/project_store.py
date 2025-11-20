"""Load and persist project path templates used across devices."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from cerebrus.config.models import ProjectDefinition, ProjectStream

LOGGER = logging.getLogger(__name__)


def _parse_streams(raw_streams: Iterable[dict]) -> list[ProjectStream]:
    return [
        ProjectStream(
            name=item["name"],
            device_subdir=item.get("device_subdir", ""),
            description=item.get("description", ""),
            include_logs=item.get("include_logs", True),
            include_csv=item.get("include_csv", True),
        )
        for item in raw_streams
    ]


def _parse_definition(raw: dict) -> ProjectDefinition:
    streams = _parse_streams(raw.get("streams", []))
    return ProjectDefinition(
        company=raw.get("company", ""),
        project=raw.get("project", ""),
        package=raw.get("package", ""),
        device_root=Path(raw.get("device_root", "/sdcard")).expanduser(),
        pc_root=Path(raw.get("pc_root", "captures")).expanduser(),
        log_dir=raw.get("log_dir", "Saved/Logs"),
        profiling_dir=raw.get("profiling_dir", "Saved/Profiling"),
        streams=streams,
        notes=raw.get("notes", ""),
    )


@dataclass(slots=True)
class ProjectStore:
    """Handle loading and caching project definitions.

    Project definitions are stored in a JSON file that can be shared outside of
    the codebase. A secondary cache file can be used to persist overrides such
    as user-selected device roots or PC destination directories without
    mutating the source file.
    """

    definition_file: Path
    cache_file: Path | None = None

    def load(self) -> list[ProjectDefinition]:
        base = self._load_file(self.definition_file)
        overrides = self._load_file(self.cache_file) if self.cache_file else []
        merged = self._merge(base, overrides)
        LOGGER.debug(
            "Loaded %d project definitions (base=%d, overrides=%d)",
            len(merged),
            len(base),
            len(overrides),
        )
        return merged

    def remember_paths(
        self,
        project: ProjectDefinition,
        *,
        device_root: Path | None = None,
        pc_root: Path | None = None,
    ) -> None:
        """Persist a partial path override for a project to the cache file."""

        if self.cache_file is None:
            LOGGER.debug("No cache file configured; skipping persistence")
            return

        overrides = {item.key: item for item in self._load_file(self.cache_file)}
        updated = overrides.get(project.key, project)
        if device_root:
            updated.device_root = device_root
        if pc_root:
            updated.pc_root = pc_root
        overrides[project.key] = updated

        payload = {
            "projects": [
                {
                    "company": item.company,
                    "project": item.project,
                    "package": item.package,
                    "device_root": str(item.device_root),
                    "pc_root": str(item.pc_root),
                    "log_dir": item.log_dir,
                    "profiling_dir": item.profiling_dir,
                    "streams": [
                        {
                            "name": stream.name,
                            "device_subdir": stream.device_subdir,
                            "description": stream.description,
                            "include_logs": stream.include_logs,
                            "include_csv": stream.include_csv,
                        }
                        for stream in item.streams
                    ],
                    "notes": item.notes,
                }
                for item in overrides.values()
            ]
        }

        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        LOGGER.info("Persisted project path overrides to %s", self.cache_file)

    # internal helpers -------------------------------------------------

    def _load_file(self, path: Path | None) -> list[ProjectDefinition]:
        if path is None or not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            LOGGER.warning("Invalid JSON in %s; ignoring file", path)
            return []

        projects = data.get("projects")
        if not projects:
            return []
        return [_parse_definition(item) for item in projects]

    @staticmethod
    def _merge(
        base: list[ProjectDefinition], overrides: list[ProjectDefinition]
    ) -> list[ProjectDefinition]:
        merged: dict[str, ProjectDefinition] = {item.key: item for item in base}
        for override in overrides:
            current = merged.get(override.key, override)
            if override.device_root:
                current.device_root = override.device_root
            if override.pc_root:
                current.pc_root = override.pc_root
            current.log_dir = override.log_dir or current.log_dir
            current.profiling_dir = override.profiling_dir or current.profiling_dir
            if override.streams:
                current.streams = override.streams
            merged[override.key] = current
        return list(merged.values())


__all__ = ["ProjectStore"]
