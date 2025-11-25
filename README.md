# Project Cerebrus

Python-based Windows-only toolkit with a Dear ImGui UI for managing Unreal Engine Android profiling workflows.

Cerebrus orchestrates:
- Device discovery and Android workload management.
- Retrieval of logcat logs, CSV profiling data, and Insights captures.
- Per-project configuration and caching.
- CSV- and PerfReport-based reporting flows using Unreal Engine's CsvTools and PerfReportTool.
- Theme configuration and a stable one-click installer.

> Note: This repository assumes you already have Unreal Engine binaries available for:
> - UAFT (Unreal Android File Tool)
> - CsvTools (CSVCollate, CsvConvert, CSVFilter, CSVSplit, CsvToSVG, csvinfo)
> - PerfReportTool

## Goals

- Deterministic, repeatable profiling workflows for Android targets.
- Clear separation of architecture, tooling wrappers, and UI.
- Codex-friendly structure and documentation.
- No hidden behavior: all automation is scripted and documented.

## Repository Layout (expected)

This scaffold assumes a layout similar to:

```text
/cerebrus/                # Core Python packages
  core/                   # Core orchestration logic and abstractions
  ui/                     # Dear ImGui UI and layout logic
  tools/                  # Wrappers around UAFT, CsvTools, PerfReportTool
  config/                 # Configuration and profile definitions
  cache/                  # Per-project cache management
  installers/             # One-click installer logic and metadata
/docs/                    # User + developer documentation
/tests/                   # Automated tests (unit + integration)
```

Adjust this layout as the project evolves, but keep documentation in sync.

## Getting Started (Developers)

1. **Clone the repository**

   ```bash
   git clone <REPO_URL> cerebrus
   cd cerebrus
   ```

2. **Create and activate a virtual environment (Windows)**

   ```bash
   py -3 -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Keep `requirements.txt` minimal and reproducible. Prefer exact versions for tooling that affects profiling reports.

4. **Configure Unreal-Tool Paths**

   Update `config/cerebrus.yaml` so that it points to your Unreal Engine
   installation binaries and declares at least one profiling profile:

   ```yaml
   version: 1
   tool_paths:
     uaft: E:/DonE/git/UE57/Engine/Binaries/Win64/UAFT.exe
     csvtools_root: E:/DonE/git/UE57/Engine/Binaries/DotNET/CsvTools
     perfreporttool: E:/DonE/git/UE57/Engine/Binaries/DotNET/CsvTools/PerfreportTool.exe
   cache:
     directory: .cerebrus-cache
   profiles:
     - name: default
       report_type: summary
       csv_filters:
         - stat=Unit
   ```

   The configuration loader validates this file on startup and injects defaults
   if the file is missing. Cerebrus wrappers consume the resolved paths rather
   than hardcoding anything.

5. **Run the toolkit scaffold**

   The repository now includes a minimal bootstrap that wires the configuration
   loader, cache manager, device manager, and UI panels together. Run it with:

   ```bash
   python -m cerebrus
   ```

   The scaffold logs panel activity and validates that configuration and cache
   directories are wired correctly. It does **not** yet render a full Dear ImGui
   experience, but it establishes the application lifecycle for follow-up work.

6. **Run preflight checks**

   Use the preflight helper to verify configuration wiring and cache creation
   without launching the UI:

   ```bash
   python -m cerebrus.core.preflight --config config/cerebrus.yaml
   ```

   If `config/cerebrus.yaml` is missing, the defaults will be used and a local
   `.cerebrus-cache` folder will be created or refreshed.

## Continuous Integration

GitHub Actions enforces three separate steps on pushes and pull requests:

1. **Lint** — `black --check`, `isort --check-only`, and `mypy` over the
   `cerebrus` package.
2. **Preflight** — `python -m cerebrus.core.preflight --config config/cerebrus.yaml`
   to ensure configuration files parse and cache directories can be created.
3. **Unit tests** — `pytest`.

Keep local changes aligned with these commands to avoid CI regressions.

## Working With Codex

Codex is the code-generation and refactoring engine for this repository. To keep changes deterministic:

- Treat Codex as a co-developer that must follow the rules in:
  - `CONTRIBUTING.md`
  - `CODEX_GUIDE.md`
  - `docs/ARCHITECTURE_OVERVIEW.md`
- Always ask Codex to:
  - Respect module boundaries.
  - Keep functions and classes small and focused.
  - Update or create documentation when modifying behavior.
  - Provide unified diffs (`@@ ... @@` blocks) when changing files.
- Prefer incremental, well-scoped tasks (e.g. refactor a single module, add one feature, etc.).

## Git Hygiene

- Default branch: `main`
- Development branch: `develop`
- Feature branches: `feature/<area>-<short-description>`
- Hotfix branches: `hotfix/<issue-id>-<short-description>`

See `CONTRIBUTING.md` for full details.

## Documentation Map

- `README.md` — high-level overview and onboarding.
- `CONTRIBUTING.md` — branching, reviews, and Codex workflow.
- `CODE_OF_CONDUCT.md` — community expectations.
- `CODEX_GUIDE.md` — how to work with Codex on this project.
- `docs/ARCHITECTURE_OVERVIEW.md` — modules and boundaries.
- `docs/CSVTOOLS_REFERENCE.md` — CsvTools usage patterns.
- `docs/PERFREPORTTOOL_REFERENCE.md` — PerfReportTool usage patterns.

Keep these up to date whenever behavior changes.
