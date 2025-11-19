# Troubleshooting

This guide lists common issues and suggested resolutions.

## Installation Issues

- **Problem**: Installer fails or Python environment not created.
  - **Check**:
    - Disk space.
    - Antivirus or security software interfering with executables.
  - **Remedy**:
    - Temporarily disable real-time scanning during install.
    - Run installer again.
    - For manual install, verify `py -3` is available on PATH.

## External Tools Not Found

- **Problem**: Cerebrus reports that UAFT or CsvTools/PerfReportTool cannot be found.
  - **Check**:
    - Paths configured in `config/tools.paths.json`.
    - That the binaries actually exist at those paths.
  - **Remedy**:
    - Correct the paths.
    - Ensure Unreal Engine installation is intact.

## No Devices Visible

- **Problem**: Device panel is empty.
  - **Check**:
    - `adb devices` from a command prompt.
    - USB debugging enabled on device.
    - Correct drivers installed.
  - **Remedy**:
    - Reconnect device and approve the host PC’s RSA key.
    - Restart ADB server: `adb kill-server` then `adb start-server`.

## Capture Failures

- **Problem**: Capture aborts or no CSV/PRC produced.
  - **Check**:
    - Device logs for crashes or permission issues.
    - Unreal project configuration for profiling (stat groups, CSV capture enabled).
  - **Remedy**:
    - Rebuild project with profiling enabled.
    - Verify correct command-line options are used to trigger CSV capture.

## Report Generation Failures

- **Problem**: PerfReportTool exits with errors.
  - **Check**:
    - Log output from PerfReportTool for missing metadata or incompatible reportType.
    - CSV integrity via `csvinfo`.
  - **Remedy**:
    - Normalize CSVs with `CsvConvert`.
    - Adjust profile configuration to use a supported `-reportType`.

When reporting issues to maintainers, include:

- Log files.
- Relevant configuration snippets.
- Exact steps to reproduce.
