"""CsvToSVG command builder."""

from __future__ import annotations

from pathlib import Path


def build_svg_args(input_csv: Path, output_svg: Path) -> list[str]:
    return [f"-Input={input_csv}", f"-Output={output_svg}"]
