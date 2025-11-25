"""State containers for the Cerebrus DearPyGui UI."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from cerebrus.core.devices import DeviceInfo


@dataclass
class UIState:
    package_name: str = ""
    profile_nickname: str = "Nickname"
    profile_path: Path = Path("/complete/path/to/profile")
    devices: List[DeviceInfo] = field(default_factory=list)
    selected_device_serial: str | None = None
    copy_directory: Path = Path("/path/to/copy")
    date_string: str = "2024-01-01"
    device_cell_tags: list[list[str]] = field(default_factory=list)
