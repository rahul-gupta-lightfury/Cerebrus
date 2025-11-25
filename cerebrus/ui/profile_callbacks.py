"""DearPyGui callbacks for profile metadata fields."""

from __future__ import annotations

from typing import Any

from cerebrus.core.state import ApplicationState
from cerebrus.ui import profile_actions


def _get_state(user_data: dict[str, Any]) -> ApplicationState:
    return user_data["state"]


def handle_profile_name_change(sender: str | int, app_data: Any, user_data: dict[str, Any]) -> None:
    """Update the active profile name when the input text changes."""
    profile_actions.set_profile_name(_get_state(user_data), str(app_data))


def handle_profile_path_change(sender: str | int, app_data: Any, user_data: dict[str, Any]) -> None:
    """Update the profile path when the input text changes."""
    profile_actions.set_profile_path(_get_state(user_data), str(app_data))


def handle_package_name_change(sender: str | int, app_data: Any, user_data: dict[str, Any]) -> None:
    """Update the package name when the input text changes."""
    profile_actions.set_package_name(_get_state(user_data), str(app_data))
