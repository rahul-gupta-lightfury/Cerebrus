# Cerebrus Delivery Roadmap

This roadmap outlines incremental phases so Codex (and contributors) can deliver UI stability, Android capture tooling, and CSV/Unreal reporting with predictable milestones. Use the branch prefixes below to keep work isolated and reviewable.

## Branching Conventions
- Start each milestone from `work`.
- Name feature branches `feature/Phase-0`, `feature/Phase-1`, `feature/Phase-2`, … to match the roadmap phases.
- Keep the branch focused on the corresponding phase scope; open a new phase branch rather than extending an older one.
- Use `QOL/<feature>` branches for quality-of-life work (for example, reintroducing profiles or path presets) so core functionality stays stable.

## Phase 0 — Launch & UI Visibility
**Goal:** Ensure the Dear PyGui dashboard reliably renders (no blank viewport) and that installers/bootstrap paths are documented.
- Verify primary-window activation order and viewport sizing on typical dev machines.
- Add diagnostics for missing/invalid Dear PyGui contexts.
- Provide quickstart notes for Windows installer + dependency bootstrap.

## Phase 1 — Device + Artifact Basics
**Goal:** Robust Android connectivity and artifact pulls for logs and CSV captures.
- Harden ADB/UAFT detection and reconnection flows.
- Support listing, filtering, and selective pulling of log/CSV files.
- Cache commonly used project paths via JSON so teams can reuse settings.

## Phase 2 — Reporting and CSV Tooling
**Goal:** Ship repeatable reporting using the packaged Unreal CSV tools.
- Wrap CsvTools binaries with parameter validation and helpful error messages.
- Emit summaries into the cache directory with clear naming.

## Phase 3 — Project Switching & UX Polish
**Goal:** Smooth multi-project handoffs and reviewer-friendly UI.
- Allow switching between multiple project JSON definitions at runtime.
- Improve panel layout (themes, sizing, sorting/filtering ergonomics).
- Expand telemetry/logging to aid support.

## Phase 4 — Stabilization & Distribution
**Goal:** Release-quality builds and automation.
- Finalize installers (Windows + cross-platform notes) with dependency checks.
- Add CI validation for config schemas and CSV tool invocations.
- Prepare release notes and distribution packaging.

---
## Quality-of-Life Backlog
- Reintroduce configurable profiling presets without hardcoded paths.
- Add optional path bookmarking and directory templates for recurring projects.
- Expose advanced filters and report presets via dedicated `QOL/<feature>` branches when ready.

---
Keep this file updated as phases complete or new needs emerge so Codex can branch correctly and target the next milestone.
