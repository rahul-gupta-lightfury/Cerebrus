# Configuration System

The configuration system provides structured access to:

- Tool paths (UAFT, CsvTools, PerfReportTool).
- Project-level settings (root paths, cache locations).
- Profiles (capture and reporting presets).

## Configuration Files

Suggested layout:

- `config/tools.paths.json`
- `config/projects/<project-name>.json`
- `config/profiles/<profile-name>.json`

Example `config/tools.paths.json`:

```json
{
  "uaft": "E:/Git/UE/Engine/Binaries/Win64/UAFT.exe",
  "csvtools_root": "E:/Git/UE/Engine/Binaries/DotNET/CsvTools",
  "perfreporttool": "E:/Git/UE/Engine/Binaries/DotNET/CsvTools/PerfreportTool.exe"
}
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
