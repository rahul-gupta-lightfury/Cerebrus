"""CSVFilter command builder."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def build_filter_args(
    input_csv: Path, output_csv: Path, filters: Iterable[str]
) -> list[str]:
    args = [f"-Input={input_csv}", f"-Output={output_csv}"]
    args.extend(filters)
    return args
