"""Application lifecycle glue for Cerebrus."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from cerebrus.cache.manager import CacheManager
from cerebrus.config.models import CerebrusConfig
from cerebrus.config.project_store import ProjectStore
from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.log_buffer import LiveLogHandler
from cerebrus.core.logging import get_logger
from cerebrus.core.projects import ProjectRegistry
from cerebrus.core.profiles import ProfileRegistry
from cerebrus.core.state import ApplicationState
from cerebrus.core.artifacts import AndroidArtifactManager
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
        project_store = ProjectStore(
            definition_file=self.config.project_paths.definition_file,
            cache_file=self.config.project_paths.cache_file,
        )
        self.project_registry = ProjectRegistry(
            store=project_store, cache_directory=self.cache_manager.config.directory
        )
        self.artifact_manager = AndroidArtifactManager(
            uaft=uaft,
            project_registry=self.project_registry,
            cache_root=self.cache_manager.config.directory,
        )
        self.ui = CerebrusUI(
            state=self.state,
            device_manager=self.device_manager,
            artifact_manager=self.artifact_manager,
        )
        self._attach_live_log_handler()

    def initialize(self) -> None:
        LOGGER.info("Initializing Cerebrus scaffold")
        self.cache_manager.ensure_cache()
        devices = self.device_manager.refresh()
        self.state.set_devices(devices)
        self.state.set_projects(self.project_registry.list_projects())
        self.state.active_profile = self.profile_registry.list_profiles()[0]

    def run(self) -> None:
        LOGGER.info("Running Cerebrus UI stub")
        self.ui.run()

    def _attach_live_log_handler(self) -> None:
        handler = LiveLogHandler(buffer=self.state.log_buffer)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logging.getLogger("cerebrus").addHandler(handler)
