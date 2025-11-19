# Theme Specification

This document specifies how themes are configured and applied in the Dear ImGui UI.

## Goals

- Provide consistent appearance across panels.
- Allow project-wide dark/light or custom themes.
- Permit advanced users to tweak colors and metrics via config files.

## Theme Configuration

- Theme config files (e.g. `config/themes/default.json`) define:
  - Color palette (background, text, accents).
  - Widget styles (button rounding, border sizes).
  - Spacing and padding.

Example (conceptual):

```json
{
  "name": "CerebrusDark",
  "colors": {
    "window_bg": [0.10, 0.10, 0.12, 1.0],
    "text": [0.95, 0.95, 0.96, 1.0],
    "accent": [0.30, 0.55, 0.90, 1.0]
  },
  "rounding": {
    "frame": 6.0,
    "window": 8.0
  },
  "spacing": {
    "item": [8.0, 4.0],
    "window_padding": [10.0, 10.0]
  }
}
```

## Application

- Theme loader module in `cerebrus/ui/theme.py`:
  - Loads theme config.
  - Applies settings to ImGui style object on startup.
  - Exposes a function to switch themes at runtime.

## Accessibility

- Provide high-contrast variants where possible.
- Avoid relying solely on color to communicate status; use icons or labels as well.
