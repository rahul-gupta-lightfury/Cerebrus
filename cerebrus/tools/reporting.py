"""Reporting helpers built on Unreal Engine CsvTools and PerfReportTool."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from cerebrus.config.models import ToolPaths
from cerebrus.core.logging import get_logger
from cerebrus.tools.base import ToolResult, run_tool
from cerebrus.tools.csv import collate, convert, filter as csv_filter, svg

LOGGER = get_logger(__name__)


def _ensure_exists(binary: Path) -> Path:
    if not binary.exists():
        raise FileNotFoundError(f"Required tool is missing: {binary}")
    return binary


@dataclass(slots=True)
class UnrealCSVToolchain:
    """Thin wrapper around the CSV binaries shipped with Unreal Engine."""

    tool_paths: ToolPaths

    def collate(self, inputs: Iterable[Path], output: Path) -> ToolResult:
        binary = _ensure_exists(self.tool_paths.resolve_csvtool("CSVCollate"))
        args = collate.build_collate_args(inputs, output)
        return run_tool(binary, args)

    def convert(self, input_csv: Path, output_csv: Path) -> ToolResult:
        binary = _ensure_exists(self.tool_paths.resolve_csvtool("CsvConvert"))
        args = convert.build_convert_args(input_csv, output_csv)
        return run_tool(binary, args)

    def apply_filter(self, input_csv: Path, output_csv: Path, filters: Iterable[str]) -> ToolResult:
        binary = _ensure_exists(self.tool_paths.resolve_csvtool("CSVFilter"))
        args = csv_filter.build_filter_args(input_csv, output_csv, filters)
        return run_tool(binary, args)

    def to_svg(self, input_csv: Path, destination: Path) -> ToolResult:
        binary = _ensure_exists(self.tool_paths.resolve_csvtool("CsvToSVG"))
        args = svg.build_svg_args(input_csv, destination)
        return run_tool(binary, args)


@dataclass(slots=True)
class ReportGenerator:
    """Bundle report generation steps for profiling CSVs."""

    toolchain: UnrealCSVToolchain
    cache_dir: Path

    def generate_summary(self, inputs: Iterable[Path], output_dir: Path | None = None) -> Path:
        output_dir = output_dir or (self.cache_dir / "reports")
        output_dir.mkdir(parents=True, exist_ok=True)

        materialized = list(inputs)
        merged_csv = output_dir / "collated.csv"
        LOGGER.info("Collating %d CSV files into %s", len(materialized), merged_csv)
        self.toolchain.collate(materialized, merged_csv).check()

        filtered_csv = output_dir / "filtered.csv"
        LOGGER.info("Applying default filters into %s", filtered_csv)
        self.toolchain.apply_filter(merged_csv, filtered_csv, filters=["stat=Unit"]).check()

        svg_output = output_dir / "graph.svg"
        LOGGER.info("Generating SVG summary at %s", svg_output)
        self.toolchain.to_svg(filtered_csv, svg_output).check()

        return svg_output


__all__ = ["ReportGenerator", "UnrealCSVToolchain"]
