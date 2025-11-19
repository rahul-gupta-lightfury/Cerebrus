"""Utility primitives for invoking external processes."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ToolResult:
    """Result of running an external binary."""

    args: Sequence[str]
    returncode: int
    stdout: str
    stderr: str

    def check(self) -> "ToolResult":
        if self.returncode != 0:
            raise RuntimeError(f"Tool failed with exit code {self.returncode}: {self.stderr}")
        return self


def run_tool(binary: Path, args: Iterable[str]) -> ToolResult:
    full_args = [str(binary), *args]
    LOGGER.debug("Executing external tool", extra={"args": full_args})
    completed = subprocess.run(
        full_args,
        capture_output=True,
        text=True,
        check=False,
    )
    result = ToolResult(
        args=tuple(full_args),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
    if completed.returncode != 0:
        LOGGER.error(
            "Tool %s failed", binary.name, extra={"stderr": completed.stderr, "args": full_args}
        )
    return result
