"""Tests for the live log buffer and handler."""

from __future__ import annotations

import logging

from cerebrus.core.log_buffer import LiveLogBuffer, LiveLogHandler


def test_live_log_buffer_caps_entries() -> None:
    buffer = LiveLogBuffer(max_lines=2)
    buffer.extend(["first", "second", "third"])
    assert buffer.snapshot() == ["second", "third"]
    buffer.clear()
    assert buffer.snapshot() == []


def test_live_log_handler_streams_formatted_logs() -> None:
    buffer = LiveLogBuffer(max_lines=10)
    handler = LiveLogHandler(buffer=buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))

    logger = logging.getLogger("cerebrus.test_live_log")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    logger.info("ui bootstrap ready")

    logger.removeHandler(handler)
    assert any("ui bootstrap ready" in line for line in buffer.snapshot())
