"""csvinfo command builder."""

from __future__ import annotations

from pathlib import Path


def build_info_args(input_csv: Path) -> list[str]:
    return [f"-Input={input_csv}"]
