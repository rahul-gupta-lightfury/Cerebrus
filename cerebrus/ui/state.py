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
    output_file_name: str = "perf_report"
    use_prefix_only: bool = False
    input_path: Path = Path("/path/to/input")
    output_path: Path = Path("/path/to/output")
    logs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            ("INFO", "Performance report initialized"),
            ("WARNING", "High memory usage detected during capture"),
            ("ERROR", "Missing frame timing data in CSV"),
            ("DEBUG", "Parsing CSV input directory"),
        ]
    )
    log_filter: str = ""
