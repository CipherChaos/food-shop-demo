import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QWidget, QSizePolicy, QStackedWidget
)
from .widgets import CircleImageLabel
from app.constants import MENU_IMAGES


class MenuItemCard(QFrame):
    add_clicked = pyqtSignal(str, int)
    decrement_clicked = pyqtSignal(str)

    def __init__(self, persian_name: str, price: int, initial_qty: int = 0, parent=None):
        super().__init__(parent)
        self.persian_name = persian_name
        self.price = price
        self.qty = initial_qty
        self.setMinimumHeight(520)
        self.setMaximumWidth(400)          # forces a portrait proportion
        self.init_ui()
        self.update_display(self.qty)

    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #fff5f7;
                border: 1px solid #f8bbd0;
                border-radius: 30px;
                padding: 12px;
            }
            QFrame:hover { background-color: #fce4ec; border-color: #ec407a; }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Image – now larger, fills ~81% of max width (260 out of 320)
        image_label = CircleImageLabel(size=260)
        image_path = MENU_IMAGES.get(self.persian_name, "")
        if image_path and os.path.exists(image_path):
            pix = QPixmap(image_path)
            if not pix.isNull():
                image_label.set_pixmap(pix)
        layout.addWidget(image_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Space between image and bottom group
        layout.addStretch(1)

        # Name + price
        name_price = QHBoxLayout()
        name_lbl = QLabel(self.persian_name)
        name_lbl.setAlignment(Qt.AlignLeft)
        name_lbl.setLayoutDirection(Qt.RightToLeft)
        name_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #4a2c2c;")
        price_lbl = QLabel(f"{self.price:,} تومان")
        price_lbl.setStyleSheet("color: #6d4c4c; font-size: 13px;")
        name_price.addWidget(name_lbl, 1)
        name_price.addWidget(price_lbl)
        layout.addLayout(name_price)

        # Controls (add button / counter)
        self.stacked = QStackedWidget()
        self.stacked.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stacked.setMinimumHeight(60)

        self.add_btn = QPushButton("+ افزودن")
        self.add_btn.setMinimumHeight(40)
        self.add_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white;
                border: none; border-radius: 8px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        self.add_btn.clicked.connect(
            lambda: self.add_clicked.emit(self.persian_name, self.price)
        )
        self.stacked.addWidget(self.add_btn)

        self.counter_widget = QWidget()
        counter_layout = QHBoxLayout(self.counter_widget)
        counter_layout.setContentsMargins(0, 0, 0, 0)
        counter_layout.setSpacing(10)

        self.minus_btn = QPushButton("-")
        self.minus_btn.setFixedSize(48, 48)
        self.minus_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8bbd0; color: #4a2c2c;
                border: none; border-radius: 22px;
                font-size: 22px; font-weight: bold;
            }
            QPushButton:hover { background-color: #ec407a; color: white; }
        """)
        self.minus_btn.clicked.connect(
            lambda: self.decrement_clicked.emit(self.persian_name)
        )

        self.qty_label = QLabel(str(self.qty))
        self.qty_label.setAlignment(Qt.AlignCenter)
        self.qty_label.setFixedWidth(50)
        self.qty_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #4a2c2c;")

        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedSize(48, 48)
        self.plus_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white;
                border: none; border-radius: 22px;
                font-size: 22px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        self.plus_btn.clicked.connect(
            lambda: self.add_clicked.emit(self.persian_name, self.price)
        )

        counter_layout.addWidget(self.minus_btn)
        counter_layout.addWidget(self.qty_label)
        counter_layout.addWidget(self.plus_btn)
        self.stacked.addWidget(self.counter_widget)

        layout.addWidget(self.stacked)

    def update_display(self, qty: int):
        self.qty = qty
        self.qty_label.setText(str(qty))
        if qty == 0:
            self.stacked.setCurrentIndex(0)
        else:
            self.stacked.setCurrentIndex(1)