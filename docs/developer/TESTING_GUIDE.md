# Testing Guide

This document outlines testing expectations and organization.

## Framework

- Use `pytest` as the primary test framework.

## Test Layout

- Mirror the `cerebrus` package:

  ```text
  tests/
    core/
    tools/
    ui/
    config/
    cache/
  ```

- Example:
  - `cerebrus/core/device_manager.py` → `tests/core/test_device_manager.py`
  - `cerebrus/tools/csv/collate.py` → `tests/tools/test_csv_collate.py`

## Types of Tests

- **Unit tests**:
  - Pure functions, config loaders, command builders.
  - No external processes or file system side effects where possible.
- **Integration tests**:
  - External tool wrappers.
  - Use temporary directories and controlled input files.

## Test Data

- Use `tests/data/` for small, synthetic CSVs and other fixtures.
- Do not commit large profiling datasets.

## Running Tests

```bash
pytest
```

Before running the full suite, keep local changes aligned with CI by executing:

```bash
black --check .
isort --check-only .
mypy cerebrus
python -m cerebrus.core.preflight
```

Optional flags:

- `-q` for quiet.
- `-k <expr>` to filter by test name.
- `-m <marker>` for groups (e.g. `slow`, `integration`).

## CI Integration

- Continuous integration should:
  - Install dependencies.
  - Run linting (`black --check`, `isort --check-only`, `mypy`).
  - Run preflight checks to validate cache creation and configuration loading.
  - Run unit tests by default.
  - Optionally run integration tests on a schedule or when requested.
