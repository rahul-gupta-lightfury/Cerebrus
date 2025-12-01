# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification file for building Cerebrus executable."""

from pathlib import Path
import sys

# Get the root directory (parent of scripts/)
root_dir = Path(SPECPATH).parent
cerebrus_dir = root_dir / "cerebrus"
binaries_dir = root_dir / "Binaries"
resources_dir = cerebrus_dir / "resources"

# Collect all resource files
datas = []

# Add resources (icons, etc.)
if resources_dir.exists():
    for resource_file in resources_dir.iterdir():
        if resource_file.is_file() and not resource_file.name.endswith('~'):
            datas.append((str(resource_file), 'cerebrus/resources'))

# Add Binaries folder if it exists
binaries = []
if binaries_dir.exists():
    for binary_file in binaries_dir.rglob('*'):
        if binary_file.is_file():
            rel_path = binary_file.relative_to(binaries_dir)
            datas.append((str(binary_file), f'Binaries/{rel_path.parent}'))

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'dearpygui',
    'dearpygui.dearpygui',
    'psutil',
    'win32api',
    'win32con',
    'win32gui',
    'pywintypes',
    'yaml',
    'requests',
]

a = Analysis(
    [str(cerebrus_dir / '__main__.py')],
    pathex=[str(root_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'mypy', 'black', 'isort'],  # Exclude dev dependencies
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Cerebrus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI application, no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(resources_dir / 'icon256x256.ico') if (resources_dir / 'icon256x256.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Cerebrus',
)
