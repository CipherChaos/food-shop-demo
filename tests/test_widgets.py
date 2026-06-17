from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMenu
from app.ui.widgets import CircleImageLabel, HoverMenuButton

class TestCircleImageLabel:
    def test_no_image_shows_placeholder(self, qapp):
        label = CircleImageLabel(size=100)
        pixmap = label.pixmap()
        assert pixmap is not None

    def test_with_image(self, qapp):
        pix = QPixmap(100, 100)
        pix.fill(QColor("red"))
        label = CircleImageLabel(pixmap=pix, size=100)
        assert label.pixmap() is not None

class TestHoverMenuButton:
    def test_setMenu(self, qapp):
        btn = HoverMenuButton()
        menu = QMenu()
        btn.setMenu(menu)
        assert btn._menu is menu

    def test_enterEvent_starts_timer(self, qapp):
        btn = HoverMenuButton()
        menu = QMenu()
        btn.setMenu(menu)
        btn.enterEvent(None)
        assert btn._hover_timer.isActive()

    def test_leaveEvent_stops_timer(self, qapp):
        btn = HoverMenuButton()
        menu = QMenu()
        btn.setMenu(menu)
        btn.enterEvent(None)
        btn.leaveEvent(None)
        assert not btn._hover_timer.isActive()