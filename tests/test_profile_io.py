import pytest
import os
from app.utils.profile_io import load_profile, save_profile

class TestProfileIO:
    def test_load_profile_returns_default_when_file_missing(self, tmp_path, monkeypatch):
        file_path = tmp_path / "nonexistent.json"
        monkeypatch.setattr("app.utils.profile_io.PROFILE_FILE", str(file_path))
        profile = load_profile()
        assert profile == {"name": "", "email": "", "phone": "", "address": "", "image_path": ""}

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        file_path = tmp_path / "profile.json"
        monkeypatch.setattr("app.utils.profile_io.PROFILE_FILE", str(file_path))
        profile = {"name": "Ali", "image_path": "/tmp/avatar.png"}
        save_profile(profile)
        loaded = load_profile()
        assert loaded["name"] == "Ali"
        assert loaded["image_path"] == "/tmp/avatar.png"