# Configuration System

The configuration system provides structured access to:

- Tool paths (UAFT, CsvTools, PerfReportTool).
- Project-level settings (root paths, cache locations).
- Profiles (capture and reporting presets).

## Configuration Files

All configuration currently lives in `config/cerebrus.yaml`. The file bundles
tool paths, cache configuration, and profile definitions into a single
schema-validated document:

```yaml
version: 1
tool_paths:
  uaft: E:/Git/UE/Engine/Binaries/Win64/UAFT.exe
  csvtools_root: E:/Git/UE/Engine/Binaries/DotNET/CsvTools
  perfreporttool: E:/Git/UE/Engine/Binaries/DotNET/CsvTools/PerfreportTool.exe
cache:
  directory: .cerebrus-cache
  max_entries: 50
profiles:
  - name: default
    report_type: summary
    csv_filters:
      - stat=Unit
```

## Loading and Validation

- A central `ConfigLoader` in `cerebrus/core/config_loader.py` should:
  - Locate config files.
  - Load JSON/YAML.
  - Validate against schema definitions in `cerebrus/config/schema.py`.
- On failure:
  - Provide clear, actionable error messages.
  - Fail fast on missing critical configuration.

## Override Mechanisms

Configuration may be overridden by:

- Environment variables (e.g. `CEREBRUS_CONFIG_ROOT`).
- Command-line arguments (e.g. `--config`).
- UI-driven overrides stored in per-user override files.

Document any overrides clearly to avoid confusion.

See `docs/config/TOOLS_PATHS.md` and `docs/config/PROFILE_DEFINITIONS.md` for more details.
