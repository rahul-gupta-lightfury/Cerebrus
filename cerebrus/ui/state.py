"""State containers for the Cerebrus DearPyGui UI."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class DeviceInfo:
    make: str
    model: str
    serial: str
    android_version: str
    sdk_level: str
    package_found: bool


@dataclass
class UIState:
    package_name: str = ""
    profile_nickname: str = "Nickname"
    profile_path: Path = Path("/complete/path/to/profile")
    devices: List[DeviceInfo] = field(default_factory=list)
    copy_directory: Path = Path("/path/to/copy")
    date_string: str = "2024-01-01"

    def sample_devices(self) -> None:
        """Populate the state with placeholder device entries."""
        self.devices = [
            DeviceInfo("Google", "Pixel 7", "192.168.1.2:5555", "14", "34", True),
            DeviceInfo("Samsung", "Galaxy S23", "R5CN90234YZ", "13", "33", False),
            DeviceInfo("OnePlus", "9 Pro", "ONEPLUS9PRO", "13", "33", True),
        ]
