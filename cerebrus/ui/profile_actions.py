"""Helper functions for DearPyGui profile interactions."""

from __future__ import annotations

from pathlib import Path

from cerebrus.config.models import ProjectProfile
from cerebrus.core.state import ApplicationState


def get_profile_fields(state: ApplicationState) -> dict[str, str]:
    """Return a mapping of profile metadata suitable for UI fields."""
    profile_name = state.active_profile.name if state.active_profile else "No profile loaded"
    profile_path = str(state.profile_path) if state.profile_path else "No profile path configured"
    package_name = state.package_name or "No package selected"
    return {
        "profile_name": profile_name,
        "profile_path": profile_path,
        "package_name": package_name,
    }


def set_profile_name(state: ApplicationState, name: str) -> None:
    """Update the active profile name, creating a placeholder profile if needed."""
    if state.active_profile is None:
        state.active_profile = ProjectProfile(name=name, report_type="", csv_filters=[], description="")
    else:
        state.active_profile.name = name


def set_profile_path(state: ApplicationState, raw_path: str) -> None:
    """Persist the profile path on the application state."""
    cleaned = raw_path.strip()
    state.profile_path = Path(cleaned) if cleaned else None


def set_package_name(state: ApplicationState, package: str) -> None:
    """Persist the package name for the active profile."""
    cleaned = package.strip()
    state.package_name = cleaned or None
