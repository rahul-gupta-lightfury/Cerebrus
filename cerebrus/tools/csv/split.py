"""CSVSplit command builder."""

from __future__ import annotations

from pathlib import Path


def build_split_args(input_csv: Path, output_dir: Path) -> list[str]:
    return [f"-Input={input_csv}", f"-Output={output_dir}"]
