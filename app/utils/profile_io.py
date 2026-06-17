import os
import json

PROFILE_FILE = "profile.json"


def load_profile() -> dict:
    """
    Load the user profile from the JSON file.
    Returns a dictionary with default values if the file is missing or invalid.
    """
    default = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "image_path": ""
    }
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Fill missing keys with defaults
                for key in default:
                    if key not in data:
                        data[key] = default[key]
                return data
        except Exception:
            pass
    return default.copy()


def save_profile(profile: dict):
    """
    Save the given profile dictionary to the JSON file.
    """
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving profile: {e}")
