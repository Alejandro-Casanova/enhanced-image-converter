import json
import logging
import os


DEFAULT_SETTINGS: dict = {
    "recent_files": [],
    "recent_folders": [],
    "presets": {},
    "last_output_dir": "",
    "theme": "light",
    "preserve_metadata": True,
    "overwrite_existing": False,
    "custom_naming": "{filename}_converted",
    "default_format": "png"
}

SETTINGS_FILE: str = os.path.join(os.path.expanduser("~"), ".image_converter_settings.json")

class SettingsManagerException(Exception):
    pass

class SettingsManager:
    def __init__(self) -> None:
        self._settings: dict = self._load_settings()
        self._logger: logging.Logger = logging.getLogger(__name__)

    def get(self, key):
        default_setting = DEFAULT_SETTINGS.get(key)
        if default_setting is None:
            raise SettingsManagerException(f"Setting '{key}' is invalid.")
        return self._settings.get(key, default_setting)

    def set(self, key, value):
        self._settings[key] = value
        self._save_settings()

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            self._logger.error(f"Error saving settings: {e}")

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            return DEFAULT_SETTINGS.copy()
        except Exception as e:
            self._logger.error(f"Error loading settings: {e}")
            return DEFAULT_SETTINGS.copy()
