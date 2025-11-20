"""Device panel stub."""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import Iterable

from cerebrus.core.device_manager import DeviceManager
from cerebrus.core.logging import get_logger
from cerebrus.core.state import ApplicationState, Device

LOGGER = get_logger(__name__)


@dataclass
class DevicePanel:
    state: ApplicationState
    device_manager: DeviceManager
    _device_table_tag: str = field(default="cerebrus-device-table")
    _status_text_tag: str = field(default="cerebrus-device-status")

    def render(self) -> None:
        devices = self.device_manager.get_connected()
        LOGGER.info("Device panel rendering %d devices", len(devices))

    # Dear PyGui helpers -------------------------------------------------
    def render_ui(self) -> None:
        import dearpygui.dearpygui as dpg

        dpg.add_text("Connected Android Devices", color=(255, 215, 0, 255))
        dpg.add_text(
            "Select an Android target for capture and reporting workflows.",
            color=(190, 190, 190, 255),
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Refresh", callback=self._on_refresh_clicked)
            dpg.add_button(label="Use First Available", callback=self._select_first_available)
            dpg.add_text("Active:")
            dpg.add_text(self._active_device_label(), tag=self._status_text_tag)

        self._build_table()

    def _build_table(self) -> None:
        import dearpygui.dearpygui as dpg

        with dpg.table(
            tag=self._device_table_tag,
            header_row=True,
            resizable=True,
            policy=dpg.mvTable_SizingStretchProp,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            borders_innerH=True,
        ):
            self._add_table_columns()
            self._populate_table_rows(self.state.devices)

    def _add_table_columns(self) -> None:
        import dearpygui.dearpygui as dpg

        dpg.add_table_column(label="Device")
        dpg.add_table_column(label="Identifier")
        dpg.add_table_column(label="Android")
        dpg.add_table_column(label="Status")

    def _populate_table_rows(self, devices: Iterable[Device]) -> None:
        import dearpygui.dearpygui as dpg

        devices_list = list(devices)

        for device in devices_list:
            with dpg.table_row(parent=self._device_table_tag):
                dpg.add_selectable(
                    label=device.model,
                    span_columns=False,
                    user_data=device.identifier,
                    callback=self._on_device_selected,
                    selected=self.state.active_device_id == device.identifier,
                )
                dpg.add_text(device.identifier)
                dpg.add_text(device.android_version)
                dpg.add_text("Ready")

        if not devices_list:
            with dpg.table_row(parent=self._device_table_tag):
                dpg.add_text("No connected devices detected", color=(200, 120, 120, 255))

    def _on_device_selected(self, sender: int, _: bool, user_data: str) -> None:
        import dearpygui.dearpygui as dpg

        self.state.set_active_device(user_data)
        self._update_status_label()
        dpg.configure_item(sender, selected=True)

    def _on_refresh_clicked(self) -> None:
        refreshed = self.device_manager.refresh()
        self.state.set_devices(refreshed)
        self._rebuild_table()
        self._update_status_label()

    def _select_first_available(self) -> None:
        first_device = self.device_manager.select_first_available()
        if first_device:
            self.state.set_active_device(first_device.identifier)
        self._rebuild_table()
        self._update_status_label()

    def _active_device_label(self) -> str:
        active_device = self.state.active_device
        if not active_device:
            return "None"
        return f"{active_device.model} ({active_device.identifier})"

    def _update_status_label(self) -> None:
        import dearpygui.dearpygui as dpg

        if not dpg.does_item_exist(self._status_text_tag):
            return
        dpg.set_value(self._status_text_tag, self._active_device_label())

    def _rebuild_table(self) -> None:
        import dearpygui.dearpygui as dpg

        if not dpg.does_item_exist(self._device_table_tag):
            return
        dpg.delete_item(self._device_table_tag, children_only=True)
        self._add_table_columns()
        self._populate_table_rows(self.state.devices)

    def sync_display(self) -> None:
        """Re-render the device rows and status label if the widgets exist."""

        import dearpygui.dearpygui as dpg

        if not dpg.does_item_exist(self._device_table_tag):
            return
        self._rebuild_table()
        self._update_status_label()
