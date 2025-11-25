"""Application lifecycle glue for Cerebrus."""

from __future__ import annotations

from dataclasses import dataclass

from cerebrus.cache.manager import CacheManager
from cerebrus.config.models import CerebrusConfig
from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.profiles import ProfileRegistry
from cerebrus.core.state import ApplicationState
from cerebrus.tools.uaft import UAFTTool
from cerebrus.ui.main_window import CerebrusUI

LOGGER = get_logger(__name__)


@dataclass
class CerebrusApp:
    """Minimal, non-UI application lifecycle."""

    config: CerebrusConfig

    def __post_init__(self) -> None:
        self.state = ApplicationState(config=self.config)
        uaft = UAFTTool(binary=self.config.tool_paths.uaft)
        self.device_manager = DeviceManager(uaft=uaft)
        self.profile_registry = ProfileRegistry(
            profiles={profile.name: profile for profile in self.config.profiles}
        )
        self.cache_manager = CacheManager(config=self.config.cache)
        self.ui = CerebrusUI(state=self.state, device_manager=self.device_manager)

    def initialize(self) -> None:
        LOGGER.info("Initializing Cerebrus scaffold")
        self.cache_manager.ensure_cache()
        devices = self.device_manager.refresh()
        self.state.set_devices(devices)
        profiles = self.profile_registry.list_profiles()
        self.state.active_profile = profiles[0] if profiles else None

    def run(self) -> None:
        LOGGER.info("Running Cerebrus UI stub")
        self.ui.render_once()
