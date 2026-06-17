from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class NotificationPopup(QFrame):
    """
    A sliding green notification bar that appears at the top right,
    auto-hides after a delay.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #66bb6a;
                border-radius: 10px;
                padding: 8px 12px;
            }
            QLabel {
                color: white;
                font-size: 15px;
                font-weight: bold;
                background: transparent;
                padding: 4px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
                border-radius: 4px;
            }
        """)
        self.setLayoutDirection(Qt.RightToLeft)
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label, 1)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self._slide_out)
        layout.addWidget(close_btn)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._slide_out)

    def show_message(self, text: str):
        """Show the notification with the given text."""
        self.label.setText(text)
        self.adjustSize()

        # Position relative to parent window
        parent_widget = self.parent()
        if parent_widget:
            x = parent_widget.width() - self.width() - 30
            y = 30
        else:
            x = 0
            y = 30
        start_y = -self.height() - 10
        self.move(x, start_y)
        self.show()

        # Slide in animation
        anim_in = QPropertyAnimation(self, b"geometry")
        anim_in.setDuration(400)
        anim_in.setEasingCurve(QEasingCurve.OutCubic)
        anim_in.setStartValue(QRect(x, start_y, self.width(), self.height()))
        anim_in.setEndValue(QRect(x, y, self.width(), self.height()))
        anim_in.start()

        fade_in = QPropertyAnimation(self, b"windowOpacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()

        self._hide_timer.start(2500)   # auto-hide after 2.5s

    def _slide_out(self):
        if not self.isVisible():
            return
        self._hide_timer.stop()

        current = self.geometry()
        end_rect = QRect(current.x(), -current.height() - 10,
                         current.width(), current.height())

        anim_out = QPropertyAnimation(self, b"geometry")
        anim_out.setDuration(300)
        anim_out.setEasingCurve(QEasingCurve.InCubic)
        anim_out.setStartValue(current)
        anim_out.setEndValue(end_rect)
        anim_out.start()

        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(200)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.start()

        anim_out.finished.connect(lambda: self.hide())
