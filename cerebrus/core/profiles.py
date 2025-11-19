"""Profile registry for Cerebrus workflows."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.config.models import ProjectProfile


@dataclass(slots=True)
class ProfileRegistry:
    """Tracks configured profiling workflows."""

    profiles: dict[str, ProjectProfile]

    def get(self, name: str) -> ProjectProfile:
        try:
            return self.profiles[name]
        except KeyError as exc:  # pragma: no cover - defensive branch
            raise KeyError(f"Profile '{name}' is not registered") from exc

    def list_profiles(self) -> list[ProjectProfile]:
        return list(self.profiles.values())
