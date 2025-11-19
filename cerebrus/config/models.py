"""Configuration dataclasses for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


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
class ProjectProfile:
    """Declarative description of a profiling workflow."""

    name: str
    report_type: str
    csv_filters: list[str] = field(default_factory=list)
    description: str = ""


@dataclass(slots=True)
class CacheConfig:
    """Configuration for cache handling."""

    directory: Path = Path(".cerebrus-cache")
    max_entries: int = 50


@dataclass(slots=True)
class CerebrusConfig:
    """Top-level configuration blob."""

    tool_paths: ToolPaths
    profiles: Sequence[ProjectProfile]
    cache: CacheConfig = field(default_factory=CacheConfig)
