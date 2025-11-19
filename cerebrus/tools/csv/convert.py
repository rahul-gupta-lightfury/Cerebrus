"""CsvConvert command builder."""

from __future__ import annotations

from pathlib import Path


def build_convert_args(input_csv: Path, output_csv: Path, *, stat: str | None = None) -> list[str]:
    args = [f"-Input={input_csv}", f"-Output={output_csv}"]
    if stat:
        args.append(f"-Stat={stat}")
    return args
