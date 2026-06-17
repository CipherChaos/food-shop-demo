import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon, QPainterPath
from PyQt5.QtWidgets import QMenu, QAction
from .widgets import HoverMenuButton


class AvatarButton(HoverMenuButton):
    """
    Circular button showing the user's profile picture (or a placeholder).
    Shows a menu on hover with options to view profile or cart.
    """
    profile_clicked = pyqtSignal()
    cart_clicked = pyqtSignal()

    def __init__(self, profile: dict, parent=None):
        super().__init__("", parent)
        self.profile = profile
        self.setFixedSize(44, 44)
        self.setStyleSheet("""
            QPushButton {
                background-color: #ec407a;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        self.clicked.connect(self._on_click)

        # Create the popup menu (also used by hover)
        self._menu = QMenu(self)
        self._menu.setLayoutDirection(Qt.RightToLeft)
        view_action = QAction("👤 مشاهده پروفایل", self)
        view_action.triggered.connect(self.profile_clicked.emit)
        self._menu.addAction(view_action)

        cart_action = QAction("🛒 سبد خرید", self)
        cart_action.triggered.connect(self.cart_clicked.emit)
        self._menu.addAction(cart_action)

        self.setMenu(self._menu)   # enables hover behavior via HoverMenuButton
        self.update_icon()

    def _on_click(self):
        """Also show the menu on explicit click."""
        pos = self.mapToGlobal(self.rect().bottomRight())
        self._menu.popup(pos)

    def update_icon(self):
        """Redraw the circular icon based on current profile data."""
        size = self.width()
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setBrush(QColor("#ec407a"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        path = self.profile.get("image_path", "")
        if path and os.path.exists(path):
            img_pix = QPixmap(path)
            if not img_pix.isNull():
                padding = 0
                image_size = size - 2 * padding
                clip_path = QPainterPath()
                clip_path.addEllipse(padding, padding, image_size, image_size)
                painter.setClipPath(clip_path)
                scaled = img_pix.scaled(image_size, image_size,
                                        Qt.KeepAspectRatioByExpanding,
                                        Qt.SmoothTransformation)
                dx = (scaled.width() - image_size) // 2
                dy = (scaled.height() - image_size) // 2
                painter.drawPixmap(padding - dx, padding - dy, scaled)
        else:
            painter.setPen(QColor("white"))
            painter.setFont(QFont("B Nazanin", 18))
            painter.drawText(pix.rect(), Qt.AlignCenter, "پروفایل")
        painter.end()
        self.setIcon(QIcon(pix))
        self.setIconSize(pix.size())
