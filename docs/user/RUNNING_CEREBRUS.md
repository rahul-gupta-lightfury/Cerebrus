# Running Cerebrus

This guide explains how to start and stop Cerebrus once installed.

## From the One-Click Installer

When installed via the one-click installer:

- Use the **Start Menu** entry “Project Cerebrus”.
- Optionally use the desktop shortcut if enabled during installation.

The application will:

- Initialize its Python environment.
- Validate configuration and external tool availability.
- Open the Dear PyGui-based UI main window.

## From Source (Developer Mode)

1. Activate your virtual environment:

   ```bash
   cd cerebrus
   .venv\Scripts\activate
   ```

2. Launch the Dear PyGui dashboard (with the live log console baked in):

   ```bash
   python -m cerebrus
   ```

   The viewport immediately mirrors the provided screenshot. It renders:

   - Overview blocks describing the active profile, cache path, and intent.
   - Connected device tiles (or a placeholder when nothing is attached).
   - Capture Session, Reports, and Environment descriptor rows with the same
     text labels shown in the reference UI.
   - A **Session Live Log** region that streams the exact logging output the
     application produces during startup and device refreshes.

## Command-Line Arguments

`python -m cerebrus` currently reserves its CLI signature for future use—the
UI launches regardless of the arguments supplied. When the toolkit needs flags
for selecting profiles or overriding configuration locations, they will be
documented here.

## Shutting Down

- Use the window close button or the **File → Exit** menu (if provided).
- Cerebrus should:
  - Flush logs.
  - Close any open file handles.
  - Stop any ongoing external tool processes gracefully.

If the UI becomes unresponsive, use the Windows Task Manager as a last resort, then inspect logs for root cause.
