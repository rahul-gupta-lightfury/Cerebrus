# Profile Definitions

Profiles describe how Cerebrus performs captures and reporting for different workflows.

## Example Profile

```yaml
- name: Android_Flythrough
  description: Default Android flythrough profiling profile.
  report_type: flythrough
  csv_filters:
    - stat=FrameTime
    - stat=GameThreadTime
```

- `name`: Unique identifier.
- `description`: Human-readable explanation.
- `report_type`: PerfReportTool `-ReportType` value.
- `csv_filters`: CsvTools filter arguments that constrain stats.

## Usage

- Profiles are listed in the UI and selectable per project.
- Capture workflows and reporting use the active profile to:
  - Filter files.
  - Select report types.
  - Choose which stats to visualize.

Define profiles carefully to reflect your project’s performance requirements.
