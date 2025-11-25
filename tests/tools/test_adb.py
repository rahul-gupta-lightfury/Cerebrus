from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from cerebrus.tools.adb import AdbClient, AdbError


def _completed(stdout: str, returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["adb"], returncode=returncode, stdout=stdout, stderr=stderr)


@patch("subprocess.run")
def test_list_devices_parses_device_lines(run_mock: MagicMock) -> None:
    run_mock.return_value = _completed("emulator-5554\tdevice\n012345\tunauthorized\nreal\tdevice")

    client = AdbClient()
    devices = client.list_devices()

    assert devices == ["emulator-5554", "real"]
    run_mock.assert_called_once_with(
        ["adb", "devices"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


@patch("subprocess.run")
def test_get_property_raises_on_failure(run_mock: MagicMock) -> None:
    run_mock.return_value = _completed("", returncode=1, stderr="boom")
    client = AdbClient()

    with pytest.raises(AdbError):
        client.get_property("serial", "ro.product.model")


@patch("subprocess.run")
def test_is_package_installed_short_circuits_for_empty_name(run_mock: MagicMock) -> None:
    client = AdbClient()

    assert client.is_package_installed("serial", "") is False
    run_mock.assert_not_called()
