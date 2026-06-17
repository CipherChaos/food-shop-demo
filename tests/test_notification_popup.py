import pytest
from app.ui.notification_popup import NotificationPopup

class TestNotificationPopup:
    @pytest.fixture
    def popup(self, qapp):
        return NotificationPopup()

    def test_show_message_changes_text(self, popup):
        popup.show_message("Test")
        assert popup.label.text() == "Test"
