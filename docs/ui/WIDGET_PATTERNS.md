# Widget Patterns

Common widget patterns to keep the UI consistent.

## Device Selector

- Multi-select table with:
  - Checkbox per row.
  - Columns: Serial, Name, OS, Status.
- Bulk actions:
  - “Select All Devices”
  - “Deselect All”

## Profile Selector

- Combo box listing available profiles.
- Show short description as tooltip.

## Path Picker

- Read-only text field for path.
- “Browse…” button to open file/directory dialog.
- Validation indicator (icon or color) when path is invalid.

## Run List

- Table of runs with:
  - Build ID.
  - Device.
  - Timestamp.
  - Result status (success/failure).
- Context menu:
  - Open folder.
  - Re-run report.
  - Compare with baseline.

Use these patterns instead of ad-hoc controls to reduce UI fragmentation.
