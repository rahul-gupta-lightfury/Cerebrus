# AI Agent Configuration for Codex (Project Cerebrus)

This file defines how Codex (and similar AI agents) should interact with this repository.

## Primary Goals

- Preserve and enforce the architecture defined in `docs/ARCHITECTURE_OVERVIEW.md`.
- Respect code standards in `CODE_STANDARDS.md`.
- Keep documentation consistent with implementation.
- Avoid destructive, large-scale refactors without explicit human approval.

## Document Map

Codex should treat the following as authoritative references:

- Top-level:
  - `README.md`
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `CODE_STANDARDS.md`
  - `CODEX_GUIDE.md`
- Architecture and tools:
  - `docs/ARCHITECTURE_OVERVIEW.md`
  - `docs/CSVTOOLS_REFERENCE.md`
  - `docs/PERFREPORTTOOL_REFERENCE.md`
- User docs:
  - `docs/user/INSTALLATION.md`
  - `docs/user/RUNNING_CEREBRUS.md`
  - `docs/user/DEVICE_CAPTURE_WORKFLOWS.md`
  - `docs/user/REPORTING_AND_ANALYSIS.md`
  - `docs/user/TROUBLESHOOTING.md`
- Developer docs:
  - `docs/developer/SETUP.md`
  - `docs/developer/PROJECT_STRUCTURE.md`
  - `docs/developer/CONFIG_SYSTEM.md`
  - `docs/developer/TOOL_WRAPPER_DESIGN.md`
  - `docs/developer/TESTING_GUIDE.md`
  - `docs/developer/LOGGING_AND_ERROR_HANDLING.md`
- UI docs:
  - `docs/ui/THEME_SPECIFICATION.md`
  - `docs/ui/IMGUI_LAYOUT_GUIDELINES.md`
  - `docs/ui/WIDGET_PATTERNS.md`
- Installer docs:
  - `docs/installer/OVERVIEW.md`
  - `docs/installer/WINDOWS_INSTALLER_SPEC.md`
- Config docs:
  - `docs/config/TOOLS_PATHS.md`
  - `docs/config/PROFILE_DEFINITIONS.md`
  - `docs/config/CACHE_MANAGEMENT.md`

## Task Scoping Rules

When receiving a request, Codex must:

1. **Identify affected modules and docs**.
2. **Limit changes** to the minimal set of files necessary.
3. Avoid repository-wide rewrites unless explicitly instructed.

Examples:

- Adding a new CsvTools wrapper:
  - Code: `cerebrus/tools/csv/<toolname>.py`
  - Tests: `tests/tools/test_csv_<toolname>.py`
  - Docs: `docs/CSVTOOLS_REFERENCE.md`, possibly `docs/developer/TOOL_WRAPPER_DESIGN.md`

- Modifying PerfReport workflow:
  - Code: `cerebrus/tools/perfreport/*`, `cerebrus/core/reporting/*`
  - Tests: `tests/tools/test_perfreport_*.py`, `tests/core/test_reporting_*.py`
  - Docs: `docs/PERFREPORTTOOL_REFERENCE.md`, `docs/config/PROFILE_DEFINITIONS.md`

## Output Requirements

Codex should:

- Prefer **unified diffs** for changes, grouped by file.
- Ensure all modified files remain syntactically valid.
- Avoid introducing unused imports, dead code, or commented-out blocks.
- Keep changes self-contained and well-described in comments and docstrings.

## Safety and Stability

Codex must:

- Preserve public APIs unless explicitly instructed to change them.
- Maintain backward compatibility for configuration formats where possible.
- Document any breaking changes clearly in:
  - `README.md` (high-level)
  - Relevant docs under `docs/developer` and `docs/config`.

## Documentation Discipline

For any non-trivial change, Codex must:

- Update or extend the relevant documentation.
- Ensure examples in docs reflect actual code.
- Avoid duplicating documentation; reference canonical locations where possible.

## Prohibited Behaviors

Codex must not:

- Introduce external network calls into the runtime code path.
- Hardcode developer-specific or machine-specific paths.
- Remove or bypass logging and error handling without replacement.

## Encouraged Patterns

- Use dataclasses and explicit models for configuration objects.
- Isolate external tool invocations in dedicated modules.
- Provide small, composable functions that are easy to test.

This configuration file should be kept up to date as the project grows and as new automation patterns emerge.
