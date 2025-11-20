"""Windows installer scaffolding."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class WindowsInstallerSpec:
    """Declarative description of what the installer should validate."""

    include_python: bool = True
    include_requirements: bool = True
    validate_adb: bool = True

    def describe(self) -> str:
        return (
            "Installer spec: include_python=%s, include_requirements=%s, validate_adb=%s"
            % (self.include_python, self.include_requirements, self.validate_adb)
        )


@dataclass(slots=True)
class InstallerReport:
    """Summarize installer actions for display in the UI."""

    python_path: str | None
    requirements_installed: bool
    adb_path: str | None
    notes: list[str]

    def to_json(self) -> str:
        payload = {
            "python_path": self.python_path,
            "requirements_installed": self.requirements_installed,
            "adb_path": self.adb_path,
            "notes": self.notes,
        }
        return json.dumps(payload, indent=2)


@dataclass(slots=True)
class WindowsInstaller:
    """Perform environment validation and dependency installation."""

    spec: WindowsInstallerSpec
    project_root: Path

    def install(self) -> InstallerReport:
        LOGGER.info("Running Windows installer with spec: %s", self.spec.describe())
        notes: list[str] = []

        python_path = self._ensure_python()
        if python_path:
            notes.append(f"Python discovered at {python_path}")

        requirements_installed = False
        if self.spec.include_requirements:
            requirements_installed = self._install_requirements(python_path)
            if requirements_installed:
                notes.append("Python requirements installed")

        adb_path = None
        if self.spec.validate_adb:
            adb_path = self._ensure_adb_on_path()
            if adb_path:
                notes.append(f"ADB available at {adb_path}")

        return InstallerReport(
            python_path=python_path,
            requirements_installed=requirements_installed,
            adb_path=adb_path,
            notes=notes,
        )

    # internals -------------------------------------------------------

    def _ensure_python(self) -> str | None:
        if not self.spec.include_python:
            return shutil.which("python")
        candidate = sys.executable or shutil.which("python") or shutil.which("py")
        if candidate:
            return candidate
        LOGGER.warning("Python interpreter not found; installer cannot proceed")
        return None

    def _install_requirements(self, python_path: str | None) -> bool:
        if python_path is None:
            return False
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            LOGGER.info("No requirements.txt found; skipping pip install")
            return True
        cmd = [python_path, "-m", "pip", "install", "-r", str(requirements_file)]
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            LOGGER.warning("pip install failed: %s", completed.stderr)
            return False
        return True

    def _ensure_adb_on_path(self) -> str | None:
        discovered = shutil.which("adb")
        if discovered:
            return discovered

        packaged = self._packaged_adb()
        if packaged:
            os.environ["PATH"] = str(packaged.parent) + os.pathsep + os.environ.get(
                "PATH", ""
            )
            return str(packaged)

        LOGGER.warning(
            "ADB was not found in PATH or the Binaries folder; UAFT operations may fail"
        )
        return None

    def _packaged_adb(self) -> Path | None:
        candidates = self._binary_candidates(["adb.exe", "adb"])
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def _binary_candidates(self, names: Iterable[str]) -> list[Path]:
        binaries_root = self.project_root / "Binaries"
        return [binaries_root / name for name in names]
