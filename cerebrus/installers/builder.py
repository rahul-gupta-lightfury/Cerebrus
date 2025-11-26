"""Utility to assemble a distributable Windows installer bundle."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable


def build_windows_installer(output_dir: Path | None = None) -> Path:
    """Create a zipped installer bundle and return the archive path.

    The bundle is structured for a Windows user-facing delivery:
    - `app/` holds the Cerebrus package, binaries, and metadata.
    - `launch_cerebrus.bat` provides a simple entry point.
    - `INSTALLER_CONTENTS.txt` records what was bundled.
    """

    repo_root = Path(__file__).resolve().parent.parent.parent
    app_source = repo_root / "cerebrus"
    binaries_source = repo_root / "Binaries"
    requirements_file = repo_root / "requirements.txt"

    if output_dir is None:
        output_dir = repo_root / "installer_output"

    staging_root = output_dir / "Cerebrus"
    app_target = staging_root / "app"

    if staging_root.exists():
        shutil.rmtree(staging_root)

    app_target.mkdir(parents=True, exist_ok=True)

    shutil.copytree(app_source, app_target / "cerebrus")

    bundled_items: list[Path | str] = [app_target / "cerebrus"]

    if binaries_source.exists():
        shutil.copytree(binaries_source, app_target / "Binaries")
        bundled_items.append(app_target / "Binaries")

    shutil.copy(requirements_file, app_target / requirements_file.name)
    bundled_items.append(requirements_file.name)

    _write_launcher(staging_root)
    _write_manifest(staging_root, bundled_items)

    archive_path = output_dir / "Cerebrus"
    if archive_path.with_suffix(".zip").exists():
        archive_path.with_suffix(".zip").unlink()

    archive_file = shutil.make_archive(str(archive_path), "zip", staging_root)
    return Path(archive_file)


def _write_launcher(staging_root: Path) -> None:
    launcher_path = staging_root / "launch_cerebrus.bat"
    launcher_content = """@echo off
setlocal
set BASE_DIR=%~dp0
set APP_DIR=%BASE_DIR%app
set PY_EXE=%APP_DIR%\\python\\python.exe

if not exist "%PY_EXE%" (
    echo No bundled Python found. Please place a Python 3.11+ build in "%APP_DIR%\\python".
    exit /b 1
)

"%PY_EXE%" -m pip install --upgrade pip --quiet
"%PY_EXE%" -m pip install -r "%APP_DIR%\\requirements.txt" --quiet
"%PY_EXE%" -m cerebrus
"""
    launcher_path.write_text(launcher_content)


def _write_manifest(staging_root: Path, items: Iterable[str | Path]) -> None:
    manifest_path = staging_root / "INSTALLER_CONTENTS.txt"
    entries = []
    for item in items:
        path = Path(item)
        entries.append(f"- {path.as_posix()}")

    manifest_lines = [
        "Cerebrus installer bundle contents:",
        "This bundle is intended for Windows distribution.",
        "Included items:",
        *entries,
        "",
        "Place a Python 3.11+ interpreter in app/python/ before running launch_cerebrus.bat.",
    ]
    manifest_path.write_text("\n".join(manifest_lines))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Cerebrus Windows installer bundle.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Directory where the installer bundle should be created (defaults to installer_output/).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    archive_path = build_windows_installer(args.output)
    print(f"Installer archive created at: {archive_path}")


if __name__ == "__main__":
    main()
