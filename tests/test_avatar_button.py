import pytest
from app.ui.avatar_button import AvatarButton

class TestAvatarButton:
    @pytest.fixture
    def avatar(self, qapp):
        profile = {"image_path": ""}
        return AvatarButton(profile)

    def test_profile_clicked_signal(self, qtbot, avatar):
        with qtbot.waitSignal(avatar.profile_clicked, timeout=500):
            avatar.profile_clicked.emit()

    def test_cart_clicked_signal(self, qtbot, avatar):
        with qtbot.waitSignal(avatar.cart_clicked, timeout=500):
            avatar.cart_clicked.emit()

    def test_update_icon_works(self, avatar):
        avatar.update_icon()
        assert avatar.icon().isNull() is False