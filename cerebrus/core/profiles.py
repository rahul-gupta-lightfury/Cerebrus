"""Registry for profiling presets configured for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from cerebrus.config.models import ProjectProfile
from cerebrus.core.logging import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ProfileRegistry:
    """Manage profiling presets declared in configuration."""

    profiles: list[ProjectProfile] = field(default_factory=list)

    def list_profiles(self) -> list[ProjectProfile]:
        return list(self.profiles)

    def set_profiles(self, profiles: Iterable[ProjectProfile]) -> None:
        self.profiles = list(profiles)
        LOGGER.info("Loaded %d profiling profiles", len(self.profiles))
