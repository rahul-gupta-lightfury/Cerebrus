from __future__ import annotations

import json
from pathlib import Path

from cerebrus.core.preflight import run_preflight


def test_preflight_creates_cache_from_config(tmp_path: Path) -> None:
    config_path = tmp_path / "cerebrus.yaml"
    cache_dir = tmp_path / "cache"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "tool_paths": {},
                "profiles": [{"name": "test", "report_type": "summary"}],
                "cache": {"directory": str(cache_dir), "max_entries": 1},
            }
        )
    )

    created_path = run_preflight(config_path)

    assert created_path == cache_dir
    assert cache_dir.exists()
    assert cache_dir.is_dir()
