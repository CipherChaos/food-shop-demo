import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFormLayout, QLineEdit, QFileDialog, QSizePolicy, QWidget
)
from .widgets import CircleImageLabel


class ProfileDialog(QDialog):
    """
    Dialog for viewing and editing the user's profile (name, email, phone, address, picture).
    """

    def __init__(self, profile_data: dict, parent=None):
        super().__init__(parent)
        self.temp_profile = profile_data.copy()
        self.original_profile = profile_data
        self.setWindowTitle("پروفایل کاربر")
        self.setModal(True)
        self.setLayoutDirection(Qt.RightToLeft)
        self.resize(400, 480)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(10)

        # Avatar section
        avatar_widget = QWidget()
        avatar_layout = QVBoxLayout(avatar_widget)
        avatar_layout.setAlignment(Qt.AlignCenter)
        avatar_layout.setSpacing(8)

        self.avatar_label = CircleImageLabel(size=280)
        img_path = self.temp_profile.get("image_path", "")
        if img_path and os.path.exists(img_path):
            pix = QPixmap(img_path)
            if not pix.isNull():
                self.avatar_label.set_pixmap(pix)

        avatar_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)

        # Upload / Remove buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        self.remove_btn = QPushButton(" حذف تصویر")
        self.remove_btn.setFixedHeight(35)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef5350; color: white;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.remove_btn.clicked.connect(self.remove_image)
        self.remove_btn.setVisible(bool(img_path) and os.path.exists(img_path))

        self.upload_btn = QPushButton(" آپلود تصویر")
        self.upload_btn.setFixedHeight(35)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        self.upload_btn.clicked.connect(self.upload_image)

        button_row.addWidget(self.remove_btn)
        button_row.addWidget(self.upload_btn)
        avatar_layout.addLayout(button_row)
        layout.addWidget(avatar_widget)

        # Form fields
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setSpacing(10)

        self.name_edit = QLineEdit(self.temp_profile.get("name", ""))
        self.email_edit = QLineEdit(self.temp_profile.get("email", ""))
        self.phone_edit = QLineEdit(self.temp_profile.get("phone", ""))
        self.address_edit = QLineEdit(self.temp_profile.get("address", ""))

        form_layout.addRow("نام:", self.name_edit)
        form_layout.addRow("ایمیل:", self.email_edit)
        form_layout.addRow("تلفن:", self.phone_edit)
        form_layout.addRow("آدرس:", self.address_edit)

        layout.addLayout(form_layout)

        # Save / Cancel buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)

        save_btn = QPushButton("ذخیره")
        save_btn.setFixedHeight(44)
        save_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white;
                border: none; border-radius: 10px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        save_btn.clicked.connect(self.save_profile)

        cancel_btn = QPushButton("انصراف")
        cancel_btn.setFixedHeight(44)
        cancel_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #9e9e9e; color: white;
                border: none; border-radius: 10px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #757575; }
        """)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(cancel_btn)   # right side (RTL)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_widget)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "انتخاب تصویر", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            pix = QPixmap(file_path)
            if not pix.isNull():
                self.avatar_label.set_pixmap(pix)
                self.temp_profile["image_path"] = file_path
                self.remove_btn.setVisible(True)

    def remove_image(self):
        self.temp_profile["image_path"] = ""
        self.avatar_label.set_pixmap(None)
        self.remove_btn.setVisible(False)

    def save_profile(self):
        self.original_profile.update(self.temp_profile)
        self.original_profile["name"] = self.name_edit.text()
        self.original_profile["email"] = self.email_edit.text()
        self.original_profile["phone"] = self.phone_edit.text()
        self.original_profile["address"] = self.address_edit.text()
        self.accept()
