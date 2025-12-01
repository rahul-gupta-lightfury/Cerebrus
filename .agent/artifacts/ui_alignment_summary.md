# UI Alignment and Font Improvements

## 1. Font Size Increase
- **New Font Setup**: Implemented `setup_fonts()` in `components.py` to load the system "Segoe UI" font.
- **Size Adjustment**: Set the default font size to 18 (up from the default ~13) to significantly improve readability across the application.
- **Integration**: Updated `app.py` to initialize fonts during startup.

## 2. Bulk Actions Alignment
- **Table Layout**: Converted the "Bulk Actions From Selected Phone to PC" and "Bulk Actions From PC to PC" sections from simple groups to 2-column tables.
- **Vertical Alignment**: This change ensures that all action buttons are perfectly aligned in the first column, and all help ("?") buttons are aligned in the second column, creating a clean, vertical column look as requested.

## 3. Tooltip Vertical Alignment
- **Spacer Removal**: Removed the manual 2px vertical spacer from the `_add_help_button` function.
- **Natural Alignment**: With the new font size and table layouts, the help buttons now align naturally with the adjacent text and buttons without needing manual offsets, resolving the "slightly out of alignment" issue.

The UI should now feature larger, easier-to-read text and a more structured, aligned layout for the bulk action buttons.
