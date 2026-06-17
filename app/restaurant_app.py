from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont

from app.core.cart_manager import CartManager
from app.ui import (MenuSection, NotificationPopup, AvatarButton,
                    ProfileDialog, CartDialog)
from app.utils.profile_io import load_profile, save_profile

class RestaurantOrderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.profile = load_profile()

        # Core components
        self.cart_manager = CartManager(self)
        self.notification = NotificationPopup(self)
        self.avatar_btn = AvatarButton(self.profile)
        self.menu_section = MenuSection(self.cart_manager)

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setWindowTitle("طعم ماندگار - سیستم مدیریت سفارش")
        self.setGeometry(100, 100, 1300, 800)
        self.setMinimumSize(1100, 700)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("""
            QMainWindow { background-color: #fce4ec; }
            QLabel { color: #4a2c2c; font-family: "B Nazanin"; }
            QPushButton { font-family: "B Nazanin"; }
            QLineEdit { font-family: "B Nazanin"; }
            QMenu::item:selected {
            background-color: #f48fb1;   /* medium pink */
            color: white;                /* optional: white text on pink */
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)
        central_widget.setLayout(main_layout)

        # Header bar
        header_widget = QWidget()
        header_widget.setStyleSheet(
            "background-color: white; border-radius: 16px; padding: 12px 20px;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 5, 10, 5)
        header_layout.setSpacing(12)

        title = QLabel("طعم ماندگار")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("B Nazanin", 24, QFont.Bold))
        title.setStyleSheet("color: #d81b60;")
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.avatar_btn)

        main_layout.addWidget(header_widget)

        # Menu section
        menu_frame = QWidget()
        menu_frame.setStyleSheet(
            "background-color: white; border-radius: 16px; padding: 18px;")
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.addWidget(self.menu_section)
        main_layout.addWidget(menu_frame)

    def connect_signals(self):
        # Menu → Cart
        self.menu_section.add_item.connect(self.cart_manager.add)
        self.menu_section.decrement_item.connect(self.cart_manager.decrement)

        # Cart → Notification
        self.cart_manager.item_added.connect(self.notification.show_message)

        # Avatar → dialogs
        self.avatar_btn.profile_clicked.connect(self.show_profile_dialog)
        self.avatar_btn.cart_clicked.connect(self.show_cart_dialog)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.notification.isVisible():
            x = self.width() - self.notification.width() - 30
            self.notification.move(x, self.notification.y())

    def show_profile_dialog(self):
        dialog = ProfileDialog(self.profile, self)
        if dialog.exec_() == dialog.Accepted:
            save_profile(self.profile)
            self.avatar_btn.update_icon()

    def show_cart_dialog(self):
        dialog = CartDialog(self.cart_manager, self.profile, self)
        dialog.exec_()
