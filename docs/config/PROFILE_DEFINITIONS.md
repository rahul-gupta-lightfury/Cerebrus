# Profile Definitions

Profiles describe how Cerebrus performs captures and reporting for different workflows.

## Example Profile

```json
{
  "name": "Android_Flythrough",
  "description": "Default Android flythrough profiling profile.",
  "reportType": "flythrough",
  "csvSearchPattern": "csvprofile_*.csv",
  "metadataFilter": "build=*;device=*",
  "charts": [
    {
      "name": "FrameTime",
      "stats": ["FrameTime", "GameThreadTime", "RenderThreadTime"]
    }
  ],
  "thresholds": {
    "FrameTime_Avg_ms": 16.6,
    "FrameTime_P95_ms": 25.0
  }
}
```

- `name`: Unique identifier.
- `description`: Human-readable explanation.
- `reportType`: PerfReportTool `-reportType` value.
- `csvSearchPattern`: Pattern used to locate CSV files for this profile.
- `metadataFilter`: Optional filter passed to CsvTools or PerfReportTool.
- `charts`: Definitions for graph presets (used by CsvToSVG).
- `thresholds`: Named thresholds for performance budget checks.

## Usage

- Profiles are listed in the UI and selectable per project.
- Capture workflows and reporting use the active profile to:
  - Filter files.
  - Select report types.
  - Choose which stats to visualize.

Define profiles carefully to reflect your project’s performance requirements.
