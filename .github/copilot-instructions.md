# Copilot Instructions for Project Cerebrus

This guide enables AI coding agents to work productively in the Cerebrus codebase. Follow these project-specific conventions and workflows for best results.

## Architecture Overview
- **Core modules:**
  - `cerebrus/core/`: Orchestration, device management, project config, profiles.
  - `cerebrus/ui/`: Dear PyGui UI panels (devices, captures, reports, config).
  - `cerebrus/tools/`: Wrappers for UAFT, CsvTools, PerfReportTool. Each tool has a dedicated submodule (see below).
  - `cerebrus/config/`: Loads/validates config from YAML/JSON, manages tool paths and overrides.
  - `cerebrus/cache/`: Per-project cache, summary tables, temp outputs.
  - `cerebrus/installers/`: Windows installer logic, environment validation.

## External Tool Wrappers
- **UAFT:** Encapsulated in `cerebrus/tools/uaft.py`. Use high-level functions like `pull_logcat(device, output_dir)`.
- **CsvTools:** Each utility (CSVCollate, CsvConvert, etc.) is wrapped in its own module under `cerebrus/tools/csv/`. Accept parameters as Python objects, not raw CLI strings.
- **PerfReportTool:** All usage in `cerebrus/tools/perfreport/`. Supports single/bulk report generation, summary export.

## Configuration
- All tool paths and project profiles are set in `config/cerebrus.yaml` and `config/projects.json`. Never hardcode developer-specific paths.
- The config loader injects defaults if files are missing and validates on startup.

## UI Patterns
- UI logic is Dear PyGui (Python bindings for Dear ImGui), organized in panels.
- UI is immediate-mode: read state, draw, then apply mutations.
- Business logic lives in `core` and `tools`; UI only calls into these modules.

## Developer Workflow
- **Setup:**
  - Create a virtualenv, install from `requirements.txt`.
  - Update config files for tool paths and project structure.
- **Run:** `python -m cerebrus` boots the dashboard UI.
- **Tests:** All tests live in `tests/` mirroring the main package structure.
- **Branching:**
  - `main`: stable, production-ready
  - `develop`: integration
  - `feature/<area>-<desc>`, `hotfix/<id>-<desc>`
- **Commits:** Use `area: summary` format. PRs must describe changes, list affected modules, and update docs/tests as needed.

## Codex/AI Collaboration
- Treat AI agents as co-developers. Follow rules in `CONTRIBUTING.md`, `CODEX_GUIDE.md`, and `docs/ARCHITECTURE_OVERVIEW.md`.
- All external tool invocations must be isolated in `cerebrus/tools/`.
- Prefer small, focused changes. Always provide rationale and unified diffs.
- Update documentation for any behavior change.

## Key References
- `README.md`: Onboarding, repo layout, setup
- `docs/ARCHITECTURE_OVERVIEW.md`: Module boundaries, integration points
- `CONTRIBUTING.md`: Branching, PRs, review process
- `CODEX_GUIDE.md`: AI agent collaboration rules
- `docs/CSVTOOLS_REFERENCE.md`, `docs/PERFREPORTTOOL_REFERENCE.md`: Tool usage patterns

## Example Patterns
- To add a new CsvTools wrapper:
  - Create `cerebrus/tools/csv/<tool>.py`.
  - Accept Python parameters, assemble CLI, capture output.
  - Add tests in `tests/tools/csv/`.
  - Update `docs/CSVTOOLS_REFERENCE.md`.
- To add a new UI panel:
  - Add to `cerebrus/ui/`, follow Dear PyGui immediate-mode.
  - Call business logic from `core`/`tools`, not directly from UI.

---

Keep this file up to date as the project evolves. Ask for clarification if any section is unclear or incomplete.
