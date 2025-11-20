from __future__ import annotations

import json
from pathlib import Path

from cerebrus.config.project_store import ProjectStore


def test_project_store_merges_overrides(tmp_path: Path) -> None:
    base_file = tmp_path / "projects.json"
    base_file.write_text(
        json.dumps(
            {
                "projects": [
                    {
                        "company": "ACME",
                        "project": "RocketGame",
                        "package": "com.acme.rocket",
                        "device_root": "Android/data/com.acme.rocket/files",
                        "pc_root": "C:/captures/rocket",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    cache_file = tmp_path / "projects.cache.json"
    cache_file.write_text(
        json.dumps(
            {
                "projects": [
                    {
                        "company": "ACME",
                        "project": "RocketGame",
                        "device_root": "/sdcard/Android/data/com.acme.rocket/files",
                        "pc_root": "D:/Perf/Rocket",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    store = ProjectStore(definition_file=base_file, cache_file=cache_file)
    projects = store.load()

    assert projects[0].device_root == Path("/sdcard/Android/data/com.acme.rocket/files")
    assert projects[0].pc_root == Path("D:/Perf/Rocket")
