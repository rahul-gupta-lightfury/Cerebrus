# Project Structure

Overview of the intended structure for the Cerebrus codebase.

```text
cerebrus/
  core/
    __init__.py
    app.py
    device_manager.py
    state.py
    config_loader.py
    profiles.py
    logging.py
  tools/
    __init__.py
    base.py
    uaft.py
    csv/
      __init__.py
      collate.py
      convert.py
      filter.py
      info.py
      split.py
      svg.py
    perfreport/
      __init__.py
      runner.py
  ui/
    __init__.py
    main_window.py
    device_panel.py
    capture_panel.py
    report_panel.py
    config_panel.py
  config/
    __init__.py
    models.py
    defaults.py
    loader.py
    schema.py
  cache/
    __init__.py
    manager.py
  installers/
    __init__.py
    windows_installer.py
tests/
  core/
  tools/
  ui/
  config/
docs/
```

This structure is aspirational but should be followed when introducing new modules.

- `core`:
  - Orchestration and high-level workflows.
- `tools`:
  - External tool wrappers only; no UI imports.
- `ui`:
  - Dear ImGui UI code; calls into `core` and `tools`.
- `config`:
  - Schema and default configuration handling.
- `cache`:
  - Handling of temporary and cached data.
- `installers`:
  - Logic required to build and run installer workflows.

Maintain this separation to keep code testable and maintainable.
