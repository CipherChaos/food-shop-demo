import pytest
from unittest.mock import patch, MagicMock
from app.ui.profile_dialog import ProfileDialog

class TestProfileDialog:
    @pytest.fixture
    def dialog(self, qapp):
        profile = {"name": "", "email": "", "phone": "", "address": "", "image_path": ""}
        return ProfileDialog(profile)

    def test_initial_fields_empty(self, dialog):
        assert dialog.name_edit.text() == ""
        assert dialog.phone_edit.text() == ""

    def test_save_updates_original(self, dialog):
        dialog.name_edit.setText("Ali")
        dialog.save_profile()
        assert dialog.original_profile["name"] == "Ali"

    @patch("app.ui.profile_dialog.QFileDialog.getOpenFileName", return_value=("test.jpg", ""))
    @patch("app.ui.profile_dialog.QPixmap", return_value=MagicMock(isNull=lambda: False))
    def test_upload_image(self, mock_pixmap, mock_dialog, dialog):
        dialog.upload_image()
        assert dialog.temp_profile["image_path"] == "test.jpg"
        assert dialog.remove_btn.isVisible()