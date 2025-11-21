# Dear ImGui C++ Bootstrap

This guide explains how to build and run the native Dear ImGui harness that seeds the PerfReport UI. The project is C++-only, uses Win32 + DirectX11, and pulls Dear ImGui from the `cerebrus/thirdparty/imgui` submodule. No CMake glue is required.

## Prerequisites

- Windows 10/11.
- Visual Studio 2022 (Desktop development with C++ workload) and the Windows 10 SDK.
- DirectX 11 runtime (included with Windows/VS).
- Git submodules pulled locally:

  ```powershell
  git submodule update --init --recursive
  ```

## Project layout

- `CerebrusImGuiApp.sln` — Visual Studio solution at the repo root.
- `cerebrus/ui/imgui_app/` — Project file, filters, and C++ sources.
- `cerebrus/thirdparty/imgui/` — Dear ImGui source (submodule, docking branch).

## Building

### Visual Studio UI

1. Open `CerebrusImGuiApp.sln` in Visual Studio 2022.
2. Choose the **x64** platform and your preferred configuration (Debug/Release).
3. Build → Build Solution.

### Developer Command Prompt

From the *x64 Native Tools Command Prompt for VS 2022*:

```batch
msbuild CerebrusImGuiApp.sln /p:Configuration=Debug /p:Platform=x64 /p:TreatWarningsAsErrors=true
```

## Running and validating

- Launch the built executable from `cerebrus/ui/imgui_app/x64/Debug/CerebrusImGuiApp.exe` (or the Release variant).
- Expect a window titled **Cerebrus Perf Report Prototype** with:
  - Input path field (CSV/PRC).
  - Output directory field.
  - Output file name field (defaults to `report.prt`).
  - **Generate Perf Report** button that updates the status line.
- Resize the window to confirm the DirectX swap chain responds correctly.

## Next integration steps

- Wire the **Generate Perf Report** action to Unreal Engine CLI tooling.
- Add logging and progress indicators to surface report-generation feedback.
- Mirror the planned layout blocks as additional ImGui windows when workflows expand.
