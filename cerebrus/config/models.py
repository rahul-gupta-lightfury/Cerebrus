"""Configuration dataclasses for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ToolPaths:
    """Paths to Unreal-provided tooling."""

    uaft: Path | None = None
    csvtools_root: Path | None = None
    perfreporttool: Path | None = None

    def resolve_csvtool(self, binary_name: str) -> Path:
        if self.csvtools_root is None:
            raise FileNotFoundError("csvtools_root is not configured")
        return self.csvtools_root / f"{binary_name}.exe"


@dataclass(slots=True)
class ProjectStream:
    """Declarative description of a per-project capture stream."""

    name: str
    device_subdir: str
    description: str = ""
    include_logs: bool = True
    include_csv: bool = True


@dataclass(slots=True)
class ProjectDefinition:
    """Persistent project metadata used to locate device artifacts."""

    company: str
    project: str
    package: str
    device_root: Path
    pc_root: Path
    log_dir: str = "Saved/Logs"
    profiling_dir: str = "Saved/Profiling"
    streams: list[ProjectStream] = field(default_factory=list)
    notes: str = ""

    @property
    def key(self) -> str:
        return f"{self.company}/{self.project}".lower()

    def device_log_path(self, stream: ProjectStream | None = None) -> Path:
        base = self.device_root / self.log_dir
        if stream and stream.device_subdir:
            return self.device_root / stream.device_subdir
        return base

    def device_profile_path(self, stream: ProjectStream | None = None) -> Path:
        base = self.device_root / self.profiling_dir
        if stream and stream.device_subdir:
            return self.device_root / stream.device_subdir
        return base


@dataclass(slots=True)
class CacheConfig:
    """Configuration for cache handling."""

    directory: Path = Path(".cerebrus-cache")
    max_entries: int = 50


@dataclass(slots=True)
class ProjectPathsConfig:
    """File locations for project path templates and overrides."""

    definition_file: Path = Path("config/projects.json")
    cache_file: Path | None = None


@dataclass(slots=True)
class CerebrusConfig:
    """Top-level configuration blob."""

    tool_paths: ToolPaths
    cache: CacheConfig = field(default_factory=CacheConfig)
    project_paths: ProjectPathsConfig = field(default_factory=ProjectPathsConfig)
