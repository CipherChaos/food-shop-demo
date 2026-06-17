from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPainterPath
from PyQt5.QtWidgets import QPushButton, QLabel, QMenu

class CircleImageLabel(QLabel):
    """A QLabel that displays an image clipped to a circle, or a placeholder."""

    def __init__(self, pixmap=None, size=360, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setScaledContents(False)
        self.pixmap = pixmap
        self.update_image()

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.update_image()

    def update_image(self):
        pix = QPixmap(self.size())
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.pixmap is not None and not self.pixmap.isNull():
            # Draw the image clipped to a perfect circle
            padding = 0
            image_size = self.width() - 2 * padding
            clip_path = QPainterPath()
            clip_path.addEllipse(padding, padding, image_size, image_size)
            painter.setClipPath(clip_path)

            scaled = self.pixmap.scaled(
                image_size, image_size,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            dx = (scaled.width() - image_size) // 2
            dy = (scaled.height() - image_size) // 2
            painter.drawPixmap(padding - dx, padding - dy, scaled)
        else:
            # Placeholder: pink circle with "پروفایل" text
            painter.setBrush(QColor("#ec407a"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, self.width(), self.height())
            painter.setPen(QColor("white"))
            painter.setFont(QFont("B Nazanin", 28))
            painter.drawText(self.rect(), Qt.AlignCenter, "پروفایل")

        painter.end()
        super().setPixmap(pix)


class HoverMenuButton(QPushButton):
    """
    A QPushButton that shows its assigned menu when the mouse hovers over it
    (with a short delay), and hides it when the mouse leaves both the button and the menu.
    """

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._menu = None
        self._hover_timer = QTimer(self)
        self._hover_timer.setSingleShot(True)
        self._hover_timer.timeout.connect(self._show_menu)
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._hide_menu)
        self._hover_delay = 200  # milliseconds

    def setMenu(self, menu: QMenu):
        """Set the menu that appears on hover (and on click)."""
        self._menu = menu

    def enterEvent(self, event):
        self._hide_timer.stop()
        if self._menu:
            self._hover_timer.start(self._hover_delay)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_timer.stop()
        if self._menu and self._menu.isVisible():
            # Allow a short time to move the cursor to the menu
            self._hide_timer.start(400)
        super().leaveEvent(event)

    def _show_menu(self):
        if self._menu and not self._menu.isVisible():
            pos = self.mapToGlobal(self.rect().bottomRight())
            self._menu.popup(pos)

    def _hide_menu(self):
        if self._menu and self._menu.isVisible():
            if not self._menu.underMouse():
                self._menu.hide()
