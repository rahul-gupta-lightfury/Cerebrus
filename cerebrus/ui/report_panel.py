"""Report panel stub."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
from cerebrus.tools.reporting import ReportGenerator, UnrealCSVToolchain

LOGGER = get_logger(__name__)


@dataclass
class ReportPanel:
    state: ApplicationState
    _generator: ReportGenerator | None = field(default=None, init=False)

    def render(self) -> None:
        LOGGER.info(
            "Report panel ready for cache dir %s and csv tools %s",
            self.state.cache_directory,
            self.state.config.tool_paths.csvtools_root,
        )

    def generate_report(self, csv_files: Iterable[Path]) -> Path | None:
        """Generate a simple SVG summary using the packaged CsvTools binaries."""

        if not self.state.config.tool_paths.csvtools_root:
            LOGGER.warning("Cannot generate reports without csvtools_root configured")
            return None

        if self._generator is None:
            toolchain = UnrealCSVToolchain(self.state.config.tool_paths)
            self._generator = ReportGenerator(
                toolchain=toolchain, cache_dir=self.state.cache_directory
            )

        return self._generator.generate_summary(csv_files)
