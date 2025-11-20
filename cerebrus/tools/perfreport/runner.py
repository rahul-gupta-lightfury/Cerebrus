"""PerfReportTool runner abstractions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cerebrus.tools.base import ToolResult, run_tool


@dataclass(slots=True)
class PerfReportSpec:
    """Arguments required to run PerfReportTool."""

    input_path: Path
    output_dir: Path
    report_type: str


@dataclass
class PerfReportRunner:
    """Execute PerfReportTool using a declarative spec."""

    binary: Path

    def run(self, spec: PerfReportSpec) -> ToolResult:
        args = [
            f"-Input={spec.input_path}",
            f"-OutputDir={spec.output_dir}",
            f"-ReportType={spec.report_type}",
        ]
        return run_tool(self.binary, args)

