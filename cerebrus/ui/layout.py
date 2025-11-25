"""DearPyGui layout primitives for the Cerebrus window."""

from __future__ import annotations

import dearpygui.dearpygui as dpg

from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState
from cerebrus.ui.components import Panel, TabContainer, Toolbar
from cerebrus.ui import profile_actions
from cerebrus.ui import profile_callbacks

LOGGER = get_logger(__name__)


class MenuBar(Toolbar):
    """Top-level application menu bar."""

    def render(self, parent: str | int | None = None) -> None:
        with dpg.menu_bar(parent=parent, tag=self.tag):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open Profile")
                dpg.add_menu_item(label="Save")
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About")
                dpg.add_menu_item(label="Documentation")


class ProfileBar(Toolbar):
    """Toolbar displaying the currently active profile metadata."""

    def __init__(self, *, state: ApplicationState, tag: str | None = None) -> None:
        super().__init__(state=state, tag=tag)

    def render(self, parent: str | int | None = None) -> None:  # noqa: D401 - clarified in base
        group = self.render_group(parent)
        fields = profile_actions.get_profile_fields(self.state)
        dpg.add_text("Profile Bar", parent=group)
        dpg.add_input_text(
            label="Profile Name",
            default_value=fields["profile_name"],
            width=300,
            parent=group,
            callback=profile_callbacks.handle_profile_name_change,
            user_data={"state": self.state},
        )
        dpg.add_input_text(
            label="Profile Path",
            default_value=fields["profile_path"],
            width=500,
            parent=group,
            callback=profile_callbacks.handle_profile_path_change,
            user_data={"state": self.state},
        )
        dpg.add_input_text(
            label="Package Name",
            default_value=fields["package_name"],
            width=300,
            parent=group,
            callback=profile_callbacks.handle_package_name_change,
            user_data={"state": self.state},
        )


class EnvDocPanel(Panel):
    """Panel describing the environment documentation placeholder."""

    def __init__(self, *, state: ApplicationState, tag: str | None = None) -> None:
        super().__init__(state=state, label="EnvDoc", tag=tag)

    def draw(self) -> None:  # noqa: D401 - clarified in base
        active_profile = self.state.active_profile.name if self.state.active_profile else "No profile"
        dpg.add_text(f"Environment documentation for: {active_profile}")
        dpg.add_separator()
        dpg.add_text("This section can be expanded with environment metadata and documentation links.")


class PerfReportPanel(Panel):
    """Stub tab for performance reports."""

    def __init__(self, *, state: ApplicationState, tag: str | None = None) -> None:
        super().__init__(state=state, label="Perf Report", tag=tag)

    def draw(self) -> None:  # noqa: D401 - clarified in base
        dpg.add_text("Performance report content will be displayed here.")
        dpg.add_spacing(count=2)
        dpg.add_text("Use this area to load and visualize performance metrics once implemented.")


class ContentTabs(TabContainer):
    """Container that aggregates the EnvDoc and Perf Report panels."""

    def __init__(self, *, state: ApplicationState) -> None:
        panels = [EnvDocPanel(state=state), PerfReportPanel(state=state)]
        super().__init__(state=state, panels=panels, tag="cerebrus_tabs")
