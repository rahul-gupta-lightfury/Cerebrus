"""UAFT tool wrapper."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

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

    def list_remote_files(self, device: Device, remote_dir: Path) -> list[Path]:
        adb = self._resolve_adb()
        if adb is None:
            LOGGER.warning("ADB not available; returning placeholder listing for %s", remote_dir)
            return [remote_dir / "placeholder.log"]

        cmd = [str(adb), "-s", device.identifier, "shell", "ls", "-1", str(remote_dir)]
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            LOGGER.warning(
                "Failed to list %s on %s (%s)", remote_dir, device.identifier, completed.stderr
            )
            return []

        files: list[Path] = []
        for line in completed.stdout.splitlines():
            candidate = line.strip()
            if candidate:
                files.append(remote_dir / candidate)
        return files

    def pull_files(
        self,
        device: Device,
        remote_dir: Path,
        destination: Path,
        *,
        files: Sequence[Path] | None = None,
    ) -> list[Path]:
        """Pull files or full directories from the device.

        When ``files`` is ``None`` the entire directory is pulled. Otherwise
        each listed file is fetched individually, allowing selective downloads
        driven by the UI.
        """

        destination.mkdir(parents=True, exist_ok=True)
        adb = self._resolve_adb()
        pulled: list[Path] = []

        if adb is None:
            LOGGER.warning("ADB not available; writing placeholders to %s", destination)
            targets = files or [remote_dir]
            for target in targets:
                placeholder = destination / Path(target).name
                placeholder.write_text("Offline placeholder", encoding="utf-8")
                pulled.append(placeholder)
            return pulled

        targets: Sequence[Path] = files or [remote_dir]
        for target in targets:
            remote_path = target if target.is_absolute() else remote_dir / target
            cmd = [str(adb), "-s", device.identifier, "pull", str(remote_path), str(destination)]
            completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if completed.returncode != 0:
                LOGGER.warning(
                    "Failed to pull %s from %s (%s)",
                    remote_path,
                    device.identifier,
                    completed.stderr,
                )
                continue
            pulled.append(destination / Path(remote_path).name)
        return pulled

    def _resolve_adb(self) -> Path | None:
        if self.binary and self.binary.exists():
            return self.binary
        discovered = shutil.which("adb")
        return Path(discovered) if discovered else None
