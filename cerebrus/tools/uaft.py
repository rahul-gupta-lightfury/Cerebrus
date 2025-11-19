"""UAFT tool wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from cerebrus.core.logging import get_logger
from cerebrus.core.state import Device

LOGGER = get_logger(__name__)


@dataclass
class UAFTTool:
    """Lightweight UAFT wrapper."""

    binary: Path | None

    def list_devices(self) -> list[Device]:
        LOGGER.info("UAFT: returning mocked device list")
        return [Device(identifier="FAKE123", model="Pixel 8", android_version="14")]

    def pull_logcat(self, device: Device, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        log_path = output_dir / f"{device.identifier}_logcat.txt"
        log_path.write_text("Logcat capture placeholder", encoding="utf-8")
        return log_path

    def pull_csv_profiles(self, device: Device, destination: Path) -> List[Path]:
        destination.mkdir(parents=True, exist_ok=True)
        fake_csv = destination / f"{device.identifier}_profile.csv"
        fake_csv.write_text("CSV placeholder", encoding="utf-8")
        return [fake_csv]
