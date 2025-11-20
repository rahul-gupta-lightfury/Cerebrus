"""Schema validation helpers for Cerebrus configuration."""

from __future__ import annotations

from typing import Any

_SCHEMA_VERSION = 1


class SchemaError(ValueError):
    """Raised when a configuration blob fails validation."""


def validate(data: dict[str, Any]) -> None:
    """Perform basic schema validation on the loaded YAML structure."""
    version = data.get("version", 1)
    if version != _SCHEMA_VERSION:
        raise SchemaError(
            f"Unsupported configuration version {version}; expected {_SCHEMA_VERSION}"
        )

    if "tool_paths" not in data:
        raise SchemaError("'tool_paths' section is required")

    if not isinstance(data.get("tool_paths"), dict):
        raise SchemaError("'tool_paths' must be a mapping")

    profiles = data.get("profiles")
    if profiles is None:
        raise SchemaError("'profiles' section is required")
    if not isinstance(profiles, list):
        raise SchemaError("'profiles' must be a list")
