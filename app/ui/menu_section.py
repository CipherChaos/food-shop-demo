from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QGridLayout, QLineEdit
)
from app.constants import MENU_DATA
from .menu_item_card import MenuItemCard


class MenuSection(QWidget):
    """
    Displays the menu grid with search bar and category buttons.
    Emits signals when the user adds or decrements items.
    """
    add_item = pyqtSignal(str, int)          # (persian_name, price)
    decrement_item = pyqtSignal(str)         # persian_name

    def __init__(self, cart_manager, parent=None):
        super().__init__(parent)
        self.cart_manager = cart_manager
        self.current_category = list(MENU_DATA.keys())[0]
        self.item_cards = {}   # persian_name -> MenuItemCard
        self.init_ui()
        # Keep widgets updated when cart changes
        cart_manager.cart_changed.connect(self.refresh_all_cards)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title
        menu_title = QLabel("منوی غذاها")
        menu_title.setAlignment(Qt.AlignCenter)
        menu_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #4a2c2c;"
        )
        main_layout.addWidget(menu_title)

        # Category buttons (centered)
        cat_widget = QWidget()
        cat_layout = QHBoxLayout(cat_widget)
        cat_layout.setContentsMargins(0, 5, 0, 5)
        cat_layout.setSpacing(12)

        categories = list(MENU_DATA.keys())
        category_names = ["پیش غذا", "غذای اصلی", "نوشیدنی", "دسر"]
        self.category_buttons = []

        cat_layout.addStretch()          # push buttons to center
        for cat, name in zip(categories, category_names):
            btn = QPushButton(name)
            btn.setFixedHeight(40)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #5d3a3a;
                    border: none;
                    border-bottom: 4px solid transparent;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #fce4ec; color: #d81b60; }
                QPushButton:checked {
                    color: #d81b60;
                    border-bottom-color: #ec407a;
                    background-color: #f8bbd0;
                }
            """)
            btn.clicked.connect(lambda checked, c=cat: self.show_category(c))
            cat_layout.addWidget(btn)
            self.category_buttons.append(btn)
        cat_layout.addStretch()          # push buttons to center
        main_layout.addWidget(cat_widget)

        # Search bar with left/right margins
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(20, 0, 20, 10)   # left/right margins
        search_layout.setSpacing(0)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("جستجوی غذا...")
        self.search_bar.setFixedHeight(38)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #f8bbd0;
                border-radius: 300000px;
                padding: 5px 20px;
                background-color: #fff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #ec407a;
                background-color: #fff5f7;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_items)
        search_layout.addWidget(self.search_bar)
        main_layout.addWidget(search_widget)

        # Scrollable grid for item cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                background: #fce4ec; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #f48fb1; border-radius: 5px; min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background: #ec407a; }
        """)
        self.container = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(15)
        self.grid.setContentsMargins(150, 0, 150, 0)
        self.container.setLayout(self.grid)
        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

        # Select first category by default
        self.category_buttons[0].setChecked(True)
        self.show_category(categories[0])

    def show_category(self, category: str):
        self.current_category = category
        self.display_items(category, self.search_bar.text())

    def filter_items(self, text: str):
        if self.current_category:
            self.display_items(self.current_category, text)

    def display_items(self, category: str, filter_text: str = ""):
        # Clear existing cards
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.item_cards.clear()

        items = MENU_DATA[category]
        row = 0
        col = 0
        max_cols = 3

        filter_text = filter_text.strip().lower()
        filtered = [(name, price) for name, price in items.items()
                    if filter_text == "" or filter_text in name.lower()]

        for persian_name, price in filtered:
            qty = self.cart_manager.quantity(persian_name)
            card = MenuItemCard(persian_name, price, qty)
            card.add_clicked.connect(self.add_item.emit)
            card.decrement_clicked.connect(self.decrement_item.emit)
            self.item_cards[persian_name] = card
            self.grid.addWidget(card, row, col, alignment=Qt.AlignVCenter)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        if not filtered:
            empty_label = QLabel("هیچ موردی یافت نشد")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet(
                "color: #999; font-size: 14px; padding: 20px;")
            self.grid.addWidget(empty_label, 0, 0, 1, max_cols)

        self.grid.setRowStretch(row + 1, 1)

    def refresh_all_cards(self):
        """Update the quantity displayed on all visible cards."""
        for name, card in self.item_cards.items():
            card.update_display(self.cart_manager.quantity(name))