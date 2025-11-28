# About Dialog Updates

## 1. Content Updates
- **Repository URL**: Updated to `https://github.com/rahul-gupta-lightfury/Cerebrus`.
- **Description**: Updated to "Python-based Windows-only toolkit with a Dear Py Gui UI for managing Unreal Engine Android profiling workflows."

## 2. UI Positioning
- **Centering**: Implemented logic to calculate the viewport center and position the "About" dialog window accordingly (`(viewport_width - window_width) // 2`, `(viewport_height - window_height) // 2`).

## 3. Versioning
- **Auto-Update**: The `cerebrus/_version.py` file is ready to be updated by your CI/CD pipeline. No changes were needed here as the mechanism remains the same. The current version is set to `0.0.1-dev`.
