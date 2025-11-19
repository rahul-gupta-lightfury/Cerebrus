"""Live logging utilities shared between the core and UI layers."""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Iterable


@dataclass(slots=True)
class LiveLogBuffer:
    """In-memory buffer that stores the last N log lines."""

    max_lines: int = 400
    _lines: Deque[str] = field(default_factory=deque)

    def append(self, line: str) -> None:
        self._lines.append(line)
        if len(self._lines) > self.max_lines:
            self._lines.popleft()

    def clear(self) -> None:
        self._lines.clear()

    def snapshot(self) -> list[str]:
        return list(self._lines)

    def extend(self, lines: Iterable[str]) -> None:
        for line in lines:
            self.append(line)

    def joined(self) -> str:
        return "\n".join(self._lines)


class LiveLogHandler(logging.Handler):
    """Logging handler that mirrors log output into a :class:`LiveLogBuffer`."""

    def __init__(self, buffer: LiveLogBuffer):
        super().__init__()
        self._buffer = buffer

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover - logging glue
        try:
            message = self.format(record)
        except Exception:  # noqa: BLE001 - logging must never raise
            message = record.getMessage()
        self._buffer.append(message)
