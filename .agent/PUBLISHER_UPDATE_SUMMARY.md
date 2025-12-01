# Publisher Information Update Summary

## Overview
Updated the build configuration to consistently identify "LeagueX Gaming" as the publisher in the application metadata.

## Changes Made

### 1. PyInstaller Specification (`scripts/cerebrus.spec`)
**Action:** Added `VSVersionInfo` block.
**Details:** 
- Embedded version information dynamically fetched from `cerebrus/_version.py`.
- Set `CompanyName` to **"LeagueX Gaming Private Limited"**.
- Set `LegalCopyright` to **"© 2025 LeagueX Gaming Private Limited"**.
- Set `FileDescription`, `ProductName`, and other standard Windows metadata fields.

### 2. Inno Setup Script (`scripts/cerebrus.iss`)
**Action:** Verified existing configuration.
**Details:**
- Confirmed `#define MyAppPublisher "LeagueX Gaming"` is present.
- This ensures the installer itself (the setup wizard) displays the correct publisher name on the welcome screen and in the Control Panel's "Add/Remove Programs" list.

## "Unknown Publisher" Warning Note
Please be aware that the "Windows protected your PC" (SmartScreen) popup showing **"Publisher: Unknown publisher"** is caused by the lack of a **Digital Code Signing Certificate**. 

Updating the text metadata (as done above) does **not** fix this specific warning. To resolve it, the executable must be cryptographically signed using a certificate purchased from a trusted Certificate Authority (CA).

However, the changes made today ensure that:
1. Right-clicking the `.exe` -> **Properties** -> **Details** will now show "LeagueX Gaming".
2. The installed program list in Windows Settings will show "LeagueX Gaming".
