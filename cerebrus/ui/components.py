"""Reusable DearPyGui UI component base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import dearpygui.dearpygui as dpg

from cerebrus.core.state import ApplicationState


class UIComponent(ABC):
    """Base class for items that render into DearPyGui."""

    def __init__(self, *, state: ApplicationState | None = None, tag: str | None = None) -> None:
        self.state = state
        self.alias = tag if isinstance(tag, str) else None
        self.tag = dpg.generate_uuid() if isinstance(tag, str) else tag

    def tag_kwargs(self) -> dict[str, Any]:
        """Return keyword arguments for DearPyGui identifiers."""

        kwargs: dict[str, Any] = {}
        if self.tag is not None:
            kwargs["tag"] = self.tag
        if self.alias is not None:
            kwargs["alias"] = self.alias
        return kwargs

    @abstractmethod
    def render(self, parent: str | int | None = None) -> None:
        """Render the component inside the provided parent."""


class Panel(UIComponent):
    """Simple tab-like panel wrapper."""

    def __init__(self, *, state: ApplicationState, label: str, tag: str | None = None) -> None:
        super().__init__(state=state, tag=tag)
        self.label = label

    @abstractmethod
    def draw(self) -> None:
        """Draw the panel contents."""

    def render(self, parent: str | int | None = None) -> None:  # noqa: D401 - clarified in base
        with dpg.tab(label=self.label, parent=parent, **self.tag_kwargs()):
            self.draw()


class TabContainer(UIComponent):
    """Container that renders multiple panels into a single tab bar."""

    def __init__(self, *, state: ApplicationState, panels: list[Panel], tag: str | None = None) -> None:
        super().__init__(state=state, tag=tag)
        self.panels = panels

    def render(self, parent: str | int | None = None) -> None:  # noqa: D401 - clarified in base
        with dpg.tab_bar(parent=parent, **self.tag_kwargs()):
            for panel in self.panels:
                panel.render()


class Toolbar(UIComponent):
    """Horizontal toolbar helper."""

    def __init__(self, *, state: ApplicationState | None = None, tag: str | None = None) -> None:
        super().__init__(state=state, tag=tag)

    def render_group(self, parent: str | int | None = None) -> Any:
        """Create the toolbar container and return its tag for child widgets."""
        return dpg.group(horizontal=True, parent=parent, **self.tag_kwargs())
