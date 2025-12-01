# Help System Implementation

## 1. User Guide Creation
- **Source**: Created `docs/user_guide.md` containing a comprehensive guide on using Cerebrus, including Profile Management, Device Management, File Actions, and Settings.
- **Generation Script**: Created `scripts/generate_docs.py` to convert the Markdown source into a styled HTML file (`cerebrus/resources/user_guide.html`). This script uses the `markdown` library and embeds CSS for a professional look.

## 2. UI Integration
- **Help Menu**: Updated the "Help" menu item to call `_open_user_guide`.
- **File Opening**: Implemented `_open_user_guide` to locate the `user_guide.html` file (handling both source and frozen/PyInstaller paths) and open it in the user's default web browser.

## 3. Build Process Integration
To ensure the help file is always up-to-date in your releases, add the following step to your build pipeline (e.g., GitHub Actions) **before** running PyInstaller:

```yaml
- name: Generate Documentation
  run: |
    pip install markdown
    python scripts/generate_docs.py
```

And ensure your PyInstaller spec file includes the `cerebrus/resources` directory. If you are using `--add-data`, it should look like:
`--add-data "cerebrus/resources;cerebrus/resources"`
