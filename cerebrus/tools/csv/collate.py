"""CSVCollate command builder."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def build_collate_args(inputs: Iterable[Path], output: Path) -> list[str]:
    args = ["-Input={}".format(path) for path in inputs]
    args.append(f"-Output={output}")
    return args
