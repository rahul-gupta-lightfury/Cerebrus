# Tool Wrapper Design

This document describes the design principles for wrapping external tools.

## Goals

- Provide a stable, testable Python API for each tool.
- Handle command-line assembly internally.
- Capture and report errors in a structured way.

## Basic Pattern

Example for CSVCollate:

```python
@dataclass
class CsvCollateConfig:
    binary_path: pathlib.Path
    default_search_pattern: str = "*.csv"

def run_collate(
    cfg: CsvCollateConfig,
    input_dir: pathlib.Path,
    output_file: pathlib.Path,
    recurse: bool = True,
    metadata_filter: str | None = None,
) -> subprocess.CompletedProcess:
    # Build argument list
    args = [str(cfg.binary_path), "-csvDir", str(input_dir), "-searchPattern", cfg.default_search_pattern]
    if recurse:
        args.append("-recurse")
    if metadata_filter:
        args.extend(["-metadataFilter", metadata_filter])
    args.extend(["-o", str(output_file)])
    # Invoke and return completed process
    ...
```

## Error Handling

- On non-zero exit code:
  - Log full command (or sanitized version).
  - Include stderr in logs.
  - Raise a specific exception or return a result object with status.

## Testing

- Unit tests for command construction:
  - Use fake paths and verify `subprocess` is called with expected arguments.
- Integration tests (optional):
  - Run real tools against small sample data where available.

See `docs/CSVTOOLS_REFERENCE.md` and `docs/PERFREPORTTOOL_REFERENCE.md` for tool-specific argument details.
