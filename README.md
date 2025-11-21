# Project Cerebrus

Native Windows toolkit built around a C++ Dear ImGui interface (Win32 + DirectX11) for driving Unreal Engine profiling workflows. The current bootstrap focuses on PerfReport generation with a simple window that captures input/output paths and emits a placeholder request status.

Cerebrus targets:
- Deterministic, repeatable profiling on Windows.
- A lightweight, C++-only UI with no CMake dependency.
- Direct references to the Dear ImGui submodule under `cerebrus/thirdparty/imgui`.

## Repository layout

```text
CerebrusImGuiApp.sln          # Visual Studio 2022 solution rooted at the repo top-level
cerebrus/ui/imgui_app/        # C++ sources and Visual Studio project
cerebrus/thirdparty/imgui/    # Dear ImGui submodule (docking branch)
docs/                         # Developer and setup documentation
```

## Getting started (Visual Studio 2022, no CMake)

1. Clone the repository and pull submodules:

   ```powershell
   git clone <REPO_URL> Cerebrus
   cd Cerebrus
   git submodule update --init --recursive
   ```

2. Open `CerebrusImGuiApp.sln` in Visual Studio 2022.
3. Select the **x64** platform and either **Debug** or **Release** configuration.
4. Build → Build Solution.
5. Run the executable from `cerebrus/ui/imgui_app/x64/<Configuration>/CerebrusImGuiApp.exe`.

You should see the **Cerebrus Perf Report Prototype** window with:
- Input path field (CSV/PRC).
- Output directory field.
- Output file name field (`report.prt` by default).
- **Generate Perf Report** button updating a status line.

## Building from the Developer Command Prompt

From the *x64 Native Tools Command Prompt for VS 2022*:

```batch
msbuild CerebrusImGuiApp.sln /p:Configuration=Debug /p:Platform=x64 /p:TreatWarningsAsErrors=true
```

Adjust the Visual Studio edition path if `msbuild` is not on your `PATH`.

## Working with Codex

- Keep the ImGui code organized under `cerebrus/ui/imgui_app/`.
- Update docs in `docs/` whenever behavior or layout changes.
- Prefer small, focused changes with clear rationale and follow-up validation steps.
