from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QMessageBox, QWidget, QBoxLayout
)
from app.utils.excel_export import export_order_to_excel


class CartDialog(QDialog):
    """
    Dialog showing the shopping cart contents, allowing quantity changes and order finalization.
    """

    def __init__(self, cart_manager, profile: dict, parent=None):
        super().__init__(parent)
        self.cart_manager = cart_manager
        self.profile = profile
        self.setWindowTitle("سبد خرید")
        self.setModal(True)
        self.setLayoutDirection(Qt.RightToLeft)
        self.resize(500, 600)
        self.init_ui()
        self.refresh_display()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Scrollable cart items
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                background: #fce4ec; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #f48fb1; border-radius: 4px; min-height: 30px;
            }
        """)
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setSpacing(10)
        self.container.setLayout(self.container_layout)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Total price label
        self.total_label = QLabel("جمع کل: ۰ تومان")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #d81b60; "
            "padding: 8px; background-color: #fce4ec; border-radius: 8px;"
        )
        layout.addWidget(self.total_label)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.clear_btn = QPushButton("پاک کردن سبد خرید")
        self.clear_btn.setFixedHeight(44)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef5350; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.clear_btn.clicked.connect(self.clear_cart)

        self.finalize_btn = QPushButton("تکمیل سفارش")
        self.finalize_btn.setFixedHeight(44)
        self.finalize_btn.setStyleSheet("""
            QPushButton {
                background-color: #66bb6a; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #43a047; }
        """)
        self.finalize_btn.clicked.connect(self.finalize_order)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.finalize_btn)
        layout.addLayout(btn_layout)

    def refresh_display(self):
        """Rebuild the list of cart items."""
        # Clear old items
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        cart = self.cart_manager.cart()
        if not cart:
            empty_label = QLabel("سبد خرید خالی است")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet(
                "color: #999; padding: 20px; font-size: 15px;")
            self.container_layout.addWidget(empty_label)
        else:
            for item in cart:
                name = item["name"]
                price = item["price"]
                qty = item["qty"]
                total = price * qty

                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: #fff5f7;
                        border: 1px solid #f8bbd0;
                        border-radius: 10px;
                        padding: 8px;
                    }
                """)
                card_layout = QVBoxLayout()
                card_layout.setSpacing(4)

                # Row with name and remove button
                top_row = QHBoxLayout()
                name_label = QLabel(name)
                name_label.setStyleSheet(
                    "font-size: 15px; font-weight: bold; color: #4a2c2c;")
                name_label.setAlignment(Qt.AlignLeft)
                name_label.setLayoutDirection(Qt.RightToLeft)
                top_row.addWidget(name_label, 1)

                remove_btn = QPushButton("🗑")
                remove_btn.setFixedSize(30, 30)
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent; color: #ef5350;
                        border: none; font-size: 16px;
                    }
                    QPushButton:hover { color: #c62828; }
                """)
                remove_btn.clicked.connect(
                    lambda checked, n=name: self.remove_item(n))
                top_row.addWidget(remove_btn)
                card_layout.addLayout(top_row)

                # Row with price and quantity controls
                bottom_row = QHBoxLayout()
                bottom_row.setSpacing(8)

                price_label = QLabel(
                    f"{price:,} تومان × {qty} = {total:,} تومان")
                price_label.setStyleSheet("color: #6d4c4c; font-size: 13px;")
                bottom_row.addWidget(price_label, 1)

                qty_controls = QHBoxLayout()
                qty_controls.setSpacing(4)

                minus_btn = QPushButton("−")
                minus_btn.setFixedSize(30, 30)
                minus_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f8bbd0; color: #4a2c2c;
                        border: none; border-radius: 15px;
                        font-size: 18px; font-weight: bold;
                    }
                    QPushButton:hover { background-color: #ec407a; color: white; }
                """)
                minus_btn.clicked.connect(
                    lambda checked, n=name: self.decrement_item(n))

                qty_label = QLabel(str(qty))
                qty_label.setAlignment(Qt.AlignCenter)
                qty_label.setFixedWidth(30)
                qty_label.setStyleSheet(
                    "font-size: 16px; font-weight: bold; color: #4a2c2c;")

                plus_btn = QPushButton("+")
                plus_btn.setFixedSize(30, 30)
                plus_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ec407a; color: white;
                        border: none; border-radius: 15px;
                        font-size: 18px; font-weight: bold;
                    }
                    QPushButton:hover { background-color: #d81b60; }
                """)
                plus_btn.clicked.connect(
                    lambda checked, n=name, p=price: self.increment_item(n, p))

                qty_controls.addWidget(minus_btn)
                qty_controls.addWidget(qty_label)
                qty_controls.addWidget(plus_btn)
                bottom_row.addLayout(qty_controls)

                card_layout.addLayout(bottom_row)
                card.setLayout(card_layout)
                self.container_layout.addWidget(card)

        self.total_label.setText(
            f"جمع کل: {self.cart_manager.total_price():,} تومان")

    # Cart modification methods (delegate to CartManager)
    def increment_item(self, name: str, price: int):
        self.cart_manager.add(name, price)
        self.refresh_display()

    def decrement_item(self, name: str):
        self.cart_manager.decrement(name)
        self.refresh_display()

    def remove_item(self, name: str):
        self.cart_manager.remove(name)
        self.refresh_display()

    def clear_cart(self):
        if not self.cart_manager.cart():
            QMessageBox.warning(self, "خطا", "سبد خرید خالی است!")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("تایید")
        dlg.setLayoutDirection(Qt.RightToLeft)
        dlg.resize(350, 120)

        layout = QVBoxLayout(dlg)
        label = QLabel("آیا از پاک کردن سبد خرید اطمینان دارید؟")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        button_layout.setDirection(QBoxLayout.RightToLeft)

        yes_btn = QPushButton("تایید")
        yes_btn.setFixedHeight(44)
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        yes_btn.clicked.connect(dlg.accept)

        no_btn = QPushButton("انصراف")
        no_btn.setFixedHeight(44)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #9e9e9e; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #757575; }
        """)
        no_btn.clicked.connect(dlg.reject)

        button_layout.addWidget(no_btn)
        button_layout.addWidget(yes_btn)

        layout.addLayout(button_layout)

        if dlg.exec_() == QDialog.Accepted:
            self.cart_manager.clear()
            self.refresh_display()

    def finalize_order(self):
        cart = self.cart_manager.cart()
        if not cart:
            QMessageBox.warning(self, "خطا", "سبد خرید خالی است!")
            return

        # Check required profile fields
        if not (self.profile.get("name") and self.profile.get("phone") and self.profile.get("address")):
            QMessageBox.warning(self, "اطلاعات ناقص",
                                "لطفاً ابتدا نام، تلفن و آدرس خود را در پروفایل تکمیل کنید.")
            return

        total = self.cart_manager.total_price()

        dlg = QDialog(self)
        dlg.setWindowTitle("تایید نهایی")
        dlg.setLayoutDirection(Qt.RightToLeft)
        dlg.resize(350, 140)

        layout = QVBoxLayout(dlg)
        label = QLabel(
            f"جمع کل سفارش: {total:,} تومان\n\nآیا از تکمیل سفارش اطمینان دارید؟")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        button_layout.setDirection(QBoxLayout.RightToLeft)

        yes_btn = QPushButton("تایید")
        yes_btn.setFixedHeight(44)
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec407a; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d81b60; }
        """)
        yes_btn.clicked.connect(dlg.accept)

        no_btn = QPushButton("انصراف")
        no_btn.setFixedHeight(44)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #9e9e9e; color: white; border: none;
                border-radius: 10px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #757575; }
        """)
        no_btn.clicked.connect(dlg.reject)

        button_layout.addWidget(no_btn)
        button_layout.addWidget(yes_btn)

        layout.addLayout(button_layout)

        if dlg.exec_() == QDialog.Accepted:
            if export_order_to_excel(cart, self):
                self.cart_manager.clear()
                self.refresh_display()
                self.accept()
