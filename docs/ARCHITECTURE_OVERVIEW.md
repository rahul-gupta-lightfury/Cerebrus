# Project Cerebrus Architecture Overview

Cerebrus is currently a native Windows Dear ImGui harness (Win32 + DirectX11) focused on Unreal Engine perf-report workflows. The codebase is C++-only and built with Visual Studio 2022—no Python runtime or CMake glue.

## Top-level components

- `CerebrusImGuiApp.sln` — Root solution file for Visual Studio 2022.
- `cerebrus/ui/imgui_app/` — C++ sources, project file, and filters for the ImGui harness.
- `cerebrus/thirdparty/imgui/` — Dear ImGui submodule (docking branch).
- `docs/` — Setup and developer documentation.

## ImGui harness responsibilities

- Render a single-window UI titled **Cerebrus Perf Report Prototype**.
- Accept:
  - Input path to CSV/PRC artifacts.
  - Output directory and file name.
- Provide a **Generate Perf Report** action (currently placeholder status updates).
- Maintain the established ImGui folder structure so third-party updates remain isolated.

## External tool expectations

Perf report generation ultimately relies on Unreal Engine tooling (e.g., PerfReportTool, CsvTools). While the current harness is UI-first, command launchers should stay modular so these tools can be integrated without disturbing the rendering or Win32/DirectX plumbing.

## Build and validation boundaries

- Visual Studio 2022 x64 configurations (Debug/Release) are the supported entry points.
- The solution references the Dear ImGui submodule directly; no additional project generators are involved.
- Keep codepaths Windows-only until a cross-platform renderer is explicitly added.

Update this document whenever new modules or integration points are introduced.
