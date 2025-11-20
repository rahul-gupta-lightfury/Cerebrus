from __future__ import annotations

import json
from pathlib import Path

from cerebrus.installers.windows_installer import WindowsInstaller, WindowsInstallerSpec


def test_installer_report_serialization(tmp_path: Path) -> None:
    spec = WindowsInstallerSpec(include_requirements=False, validate_adb=False)
    installer = WindowsInstaller(spec=spec, project_root=tmp_path)

    report = installer.install()
    payload = json.loads(report.to_json())

    assert "python_path" in payload
    assert payload["requirements_installed"] is False or isinstance(
        payload["requirements_installed"], bool
    )
