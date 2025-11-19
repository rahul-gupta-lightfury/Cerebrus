"""Windows installer scaffolding."""

from __future__ import annotations

from dataclasses import dataclass


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
