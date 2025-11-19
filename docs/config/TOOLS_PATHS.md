# Tools Paths Configuration

This document describes how to configure paths to external tools.

## Config File

Use `config/tools.paths.json` to specify paths:

```json
{
  "uaft": "E:/Git/UE/Engine/Binaries/Win64/UAFT.exe",
  "csvtools_root": "E:/Git/UE/Engine/Binaries/DotNET/CsvTools",
  "perfreporttool": "E:/Git/UE/Engine/Binaries/DotNET/CsvTools/PerfreportTool.exe"
}
```

- `uaft`: Full path to `UAFT.exe`.
- `csvtools_root`: Directory containing `CSVCollate.exe`, `CsvConvert.exe`, `CSVFilter.exe`, `CSVSplit.exe`, `CsvToSVG.exe`, `csvinfo.exe`, and `PerfreportTool.exe`.
- `perfreporttool`: Explicit path to `PerfreportTool.exe`; if omitted, derived from `csvtools_root`.

## Validation

- On startup, Cerebrus should:
  - Confirm the existence of `uaft` (if required for your workflow).
  - Confirm the existence of `CSVCollate.exe` and `PerfreportTool.exe`.
  - Log warnings for missing tools and disable corresponding features.

Update this file when Unreal Engine or tools are moved or upgraded.
