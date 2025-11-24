# Code Standards for Project Cerebrus

This document defines the baseline coding standards for all Python and configuration code in this repository.

## Languages and Versions

- Python:
  - Target: **Python 3.11+** on Windows.
  - Assume 64-bit environment.
- OS:
  - Windows 10 or newer (64-bit).

## C++ (Dear ImGui app)

- Target: C++17 for the Dear ImGui Win32/DX11 sample in `cerebrus/ui/imgui_app`.
- File naming: use PascalCase/AllmanCase for translation units and headers (e.g., `Main.cpp`, `PerfReportWindow.h`).
- Formatting and structure:
  - Allman style braces: open braces on their own line for classes, methods, functions, and control statements.
  - Avoid namespaces across the ImGui layer and broader codebase unless explicitly required by an external library; prefer free functions and file-static helpers.
  - Keep functions small and focused on a single responsibility.
- Naming:
  - Prefix global variables and constants with `g_`; consolidate shared values (e.g., UI dimensions, default key bindings) in a dedicated global header to prevent magic numbers.
  - Data members use camel case with an `m_` prefix (e.g., `m_InputPath`, `m_RequestSubmitted`).
  - Prefer descriptive method names such as `RenderMenuBar`, `ApplyDarkGreen`, or `QueueRequest`.
- Dependencies and includes:
  - Include only what you use; keep headers minimal and prefer forward declarations when practical.
  - Never wrap `#include` directives in `try/catch` blocks.
- ImGui specifics:
  - Configure docking explicitly via `ImGuiIO::ConfigFlags` and maintain a viewport-level dockspace in the main frame.
  - Centralize style/theming changes in a dedicated helper (e.g., `Theme::ApplyDarkGreen`).

## General Principles

- Prefer **clarity over cleverness**.
- Keep functions **small and focused**; aim for a single responsibility.
- Design for **testability**: separate pure logic from I/O and process invocation.
- Avoid premature optimization; optimize only when you have measurements.
- Do not introduce new dependencies without justification.

## Project Structure

- Core layout (logical):

  - `cerebrus/core` – orchestration, config, state models.
  - `cerebrus/ui` – Dear PyGui UI only; no direct process spawning.
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

  from dearpygui import dearpygui as dpg
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

All new code should pass the standard format and lint checks.

## Commit Discipline

- Keep commits focused on a single logical change.
- Do not mix refactors with feature changes where possible.
- Update tests and docs in the same PR as behavior changes.

This document takes precedence when there is ambiguity. When in doubt, favor consistency with existing code.
