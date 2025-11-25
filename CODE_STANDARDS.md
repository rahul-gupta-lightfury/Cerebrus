# Code Standards for Project Cerebrus

This document defines the baseline coding standards for all Python and configuration code in this repository.

## Languages and Versions

- Python:
  - Target: **Python 3.11+** on Windows.
  - Assume 64-bit environment.
- OS:
  - Windows 10 or newer (64-bit).

## General Principles

- Prefer **clarity over cleverness**.
- Keep functions **small and focused**; aim for a single responsibility.
- Design for **testability**: separate pure logic from I/O and process invocation.
- Avoid premature optimization; optimize only when you have measurements.
- Do not introduce new dependencies without justification.

## Project Structure

- Core layout (logical):

  - `cerebrus/core` – orchestration, config, state models.
  - `cerebrus/ui` – Dear ImGui UI only; no direct process spawning.
  - `cerebrus/tools` – thin wrappers around external tools (UAFT, CsvTools, PerfReportTool, etc.).
  - `cerebrus/config` – configuration loading, schema validation, and profile management.
- `cerebrus/cache` – cache operations and clean-up routines.
  - `cerebrus/installers` – installer logic and environment checks.
  - `tests` – mirrors source layout.

No module in `ui` may import `subprocess` or call external tools directly; this must go through `core` and `tools`.

## Python Style

- Follow **PEP 8** where practical.
- Use **type hints** everywhere:
  - Public functions and methods must have full type annotations.
  - Use `typing.Protocol` and `TypedDict` where appropriate.
- Use **dataclasses** for simple data containers.
- Avoid global state; prefer explicit dependency passing or small factories.

### Imports

- Standard library imports first, then third-party, then local imports:

  ```python
  import pathlib
  import subprocess
  from dataclasses import dataclass

  import imgui
  import psutil

  from cerebrus.core.device import Device
  from cerebrus.tools.csv import collate
  ```

- Use absolute imports within the `cerebrus` package.

### Error Handling

- Never silently swallow exceptions.
- Wrap external tool calls (`subprocess`) and:
  - Capture `stdout`, `stderr`, and exit code.
  - Raise structured exceptions or return structured results.
- UI layer should translate exceptions into user-facing messages; lower layers must not depend on UI.

### Logging

- Use a central logging facility (e.g. the standard `logging` module wrapped in `cerebrus.core.logging`).
- Log:
  - Entry/exit for major workflows.
  - External tool invocations (sanitized arguments).
  - Non-zero exit codes and error output.
- Avoid log spam; use levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) correctly.

## Testing

- Use `pytest`.
- For each module in `cerebrus/`, maintain corresponding tests in `tests/`.
- Separate:
  - **Unit tests**: pure functions, config parsing, command-building for tools.
  - **Integration tests**: optional, for running external tools in controlled environments.
- Tests should not require network connectivity or write to arbitrary user locations.

## External Tools Wrappers

- All external tools (UAFT, CsvTools, PerfReportTool, etc.) must:
  - Be wrapped by small, focused Python modules in `cerebrus.tools`.
  - Use **dependency injection** for the binary path.
  - Expose high-level functions that accept data structures, not raw CLI argument lists.
- Do not construct command strings in the UI or core layers.

## Configuration Files

- Prefer **YAML** or **JSON** for configuration.
- Provide example files under `docs/config` and/or `config/examples`.
- Enforce schema via central validation before using config values.

## Style Tools

- Use:
  - `black` for formatting.
  - `isort` for import ordering.
  - `mypy` for static type checking.
  - `flake8` or `ruff` for linting (config to be added).

## Cache Management

- Use `cerebrus.cache.CacheManager` for any file-system level cache handling.
- Respect `CacheConfig.max_entries` when writing cache helpers; avoid unbounded growth.
- New cache logic must include unit tests under `tests/cache/`.

## CI Expectations

- GitHub Actions runs three distinct steps:
  - **Lint** (`black --check`, `isort --check-only`, `mypy`).
  - **Preflight** (`python -m cerebrus.core.preflight`) to validate configuration wiring and cache creation.
  - **Unit tests** (`pytest`).
- Keep local changes aligned with these checks to avoid CI regressions.

All new code should pass the standard format and lint checks.

## Commit Discipline

- Keep commits focused on a single logical change.
- Do not mix refactors with feature changes where possible.
- Update tests and docs in the same PR as behavior changes.

This document takes precedence when there is ambiguity. When in doubt, favor consistency with existing code.
