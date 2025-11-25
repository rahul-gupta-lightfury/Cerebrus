"""Core orchestration utilities for Cerebrus.

Lazy attribute access avoids expensive imports during module initialization.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["CerebrusApp", "DeviceManager", "ProfileRegistry"]


def __getattr__(name: str) -> Any:
    if name == "CerebrusApp":
        return import_module("cerebrus.core.app").CerebrusApp
    if name == "DeviceManager":
        return import_module("cerebrus.core.device_manager").DeviceManager
    if name == "ProfileRegistry":
        return import_module("cerebrus.core.profiles").ProfileRegistry
    raise AttributeError(f"module 'cerebrus.core' has no attribute '{name}'")
