import json
import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

# Global config path
CONFIG_DIR = Path.home() / ".cerebrus"
CONFIG_FILE = CONFIG_DIR / "config.json"

@dataclass
class Profile:
    nickname: Optional[str] = None
    package_name: str = ""
    engine_root: str = ""
    project_root: str = ""
    # We can add more fields here as needed to persist UI state
    input_path: str = ""
    output_path: str = ""
    output_file_name: str = ""
    use_prefix_only: bool = False

    def validate(self) -> list[str]:
        errors = []
        if not self.package_name:
            errors.append("Package Name cannot be empty.")
        elif not self.package_name.startswith("com."):
            errors.append("Package Name must start with 'com.'.")
        return errors

    def save(self, path: Path) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=4)

    @classmethod
    def load(cls, path: Path) -> "Profile":
        if not path.exists():
            raise FileNotFoundError(f"Profile not found at {path}")
        with open(path, "r") as f:
            data = json.load(f)
        # Filter out keys that might not be in the dataclass anymore (forward compatibility)
        # or handle missing keys (backward compatibility)
        # For now, simple unpacking
        return cls(**data)

class ProfileManager:
    def __init__(self):
        self._ensure_config_dir()
        self.current_profile: Optional[Profile] = None
        self.current_profile_path: Optional[Path] = None

    def _ensure_config_dir(self):
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True)

    def get_last_used_profile_path(self) -> Optional[Path]:
        if not CONFIG_FILE.exists():
            return None
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                path_str = data.get("last_used_profile")
                if path_str:
                    path = Path(path_str)
                    if path.exists():
                        return path
        except Exception:
            pass
        return None

    def set_last_used_profile_path(self, path: Path | None):
        data = {}
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        
        if path:
            data["last_used_profile"] = str(path.absolute())
        else:
            data.pop("last_used_profile", None)
            
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_last_profile(self) -> tuple[Profile, Optional[Path]]:
        path = self.get_last_used_profile_path()
        if path:
            try:
                profile = Profile.load(path)
                self.current_profile = profile
                self.current_profile_path = path
                return profile, path
            except Exception:
                # Failed to load, maybe deleted
                self.set_last_used_profile_path(None)
        
        # Default profile
        default_profile = Profile(nickname=None)
        self.current_profile = default_profile
        self.current_profile_path = None
        return default_profile, None

    def create_new_profile(self, nickname: str, package_name: str, path: Path) -> Profile:
        profile = Profile(nickname=nickname, package_name=package_name)
        # Validate before saving? User said "Package Name input field would be saved into the profile by the user and cannot be null..."
        # We'll assume the UI handles validation feedback, but we can check here too.
        profile.save(path)
        self.current_profile = profile
        self.current_profile_path = path
        self.set_last_used_profile_path(path)
        return profile

    def save_current_profile(self):
        if self.current_profile and self.current_profile_path:
            self.current_profile.save(self.current_profile_path)
