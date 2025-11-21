# Cerebrus ImGui (C++) Bootstrap

A Win32 + DirectX11 Dear ImGui harness that seeds the Cerebrus perf-report UI. The prototype opens a single window with:

- An input path field for the CSV/PRC artifact.
- An output directory field.
- An output file name field.
- A **Generate Perf Report** button that records a placeholder request status.

The project keeps the existing ImGui folder layout (`cerebrus/thirdparty/imgui` submodule) and avoids introducing CMake.

## Prerequisites

- Visual Studio 2022 with the **Desktop development with C++** workload and the Windows 10 SDK.
- DirectX 11 runtime (ships with Windows 10/11 and Visual Studio toolchains).
- Git submodule contents present:

  ```powershell
  git submodule update --init --recursive
  ```

## Building and running (no CMake)

1. Open the root solution `CerebrusImGuiApp.sln` in Visual Studio 2022.
2. Select the **x64** platform and either **Debug** or **Release** configuration.
3. Build the solution (Build → Build Solution or `Ctrl+Shift+B`).
4. Run the application (Debug → Start Debugging or `F5`). The window title is **Cerebrus Perf Report Prototype**.

### Command-line build via Developer Command Prompt

If you prefer not to open the IDE, use the *x64 Native Tools Command Prompt for VS 2022*:

```batch
msbuild CerebrusImGuiApp.sln /p:Configuration=Debug /p:Platform=x64 /p:TreatWarningsAsErrors=true
```

## Next steps

- Wire the **Generate Perf Report** button to the Unreal Engine PerfReportTool command line once available.
- Extend the layout to mirror planned panels (device selection, capture flows, status console).
- Add automated smoke tests once the build pipeline is defined.
