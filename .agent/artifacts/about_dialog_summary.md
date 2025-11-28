# About Dialog Implementation

## 1. Version Management
- **File Created**: `cerebrus/_version.py`
- **Purpose**: Stores the application version string (`__version__`).
- **Auto-Update**: This file is designed to be updated by your CI/CD pipeline (e.g., GitHub Actions) during the release process. You can use a script to replace the version string with the git tag before building the executable.

## 2. UI Updates
- **Menu Item**: Added functionality to the "About" item in the "Help" menu.
- **Dialog Content**: Implemented `_show_about_dialog` to display:
  - **App Name**: Cerebrus
  - **Version**: Loaded dynamically from `_version.py`
  - **Author**: Lightfury Games (Rahul Gupta)
  - **Repository**: https://github.com/rahulguptagamedev/Aegis-A-UE-GUI-Toolbelt-for-UE-CLI
  - **Description**: A UE GUI toolbelt for Unreal Engine command-line tools.
  - **License**: Apache 2.0 License

## 3. How to Automate Versioning
To automate the version update in your GitHub Actions workflow, add a step before the build process:

```yaml
- name: Update Version
  run: |
    echo "__version__ = '${{ github.ref_name }}'" > cerebrus/_version.py
  shell: bash
```
This will overwrite `_version.py` with the current git tag (e.g., "v1.0.0") before the application is compiled.
