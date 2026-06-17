from PyQt5.QtCore import QObject, pyqtSignal


class CartManager(QObject):
    """
    Manages the shopping cart data.
    Emits signals on any change so UI components can react.
    """
    cart_changed = pyqtSignal()          # emitted whenever the cart is modified
    # provides a notification text (name added)
    item_added = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cart = []

    # Public API

    def cart(self):
        """Return a copy of the current cart list."""
        return self._cart[:]

    def set_cart(self, new_cart):
        """Replace the entire cart (rarely used externally)."""
        self._cart = new_cart
        self.cart_changed.emit()

    def add(self, name: str, price: int):
        """
        Add one item to the cart. If the item already exists, increment its quantity.
        Emits cart_changed and item_added (with a Persian notification).
        """
        for item in self._cart:
            if item["name"] == name:
                item["qty"] += 1
                self.cart_changed.emit()
                self.item_added.emit(f"{name} به سبد خرید اضافه شد")
                return
        self._cart.append({"name": name, "price": price, "qty": 1})
        self.cart_changed.emit()
        self.item_added.emit(f"{name} به سبد خرید اضافه شد")

    def decrement(self, name: str):
        """
        Decrease the quantity of an item by one.
        If quantity becomes 0, remove the item.
        """
        for item in self._cart:
            if item["name"] == name:
                if item["qty"] > 1:
                    item["qty"] -= 1
                else:
                    self._cart.remove(item)
                self.cart_changed.emit()
                return

    def remove(self, name: str):
        """Completely remove an item from the cart."""
        self._cart = [i for i in self._cart if i["name"] != name]
        self.cart_changed.emit()

    def clear(self):
        """Empty the cart."""
        self._cart.clear()
        self.cart_changed.emit()

    def quantity(self, name: str) -> int:
        """Return the current quantity of a given item (0 if not in cart)."""
        for item in self._cart:
            if item["name"] == name:
                return item["qty"]
        return 0

    def total_price(self) -> int:
        """Calculate the total price of all items in the cart."""
        return sum(item["price"] * item["qty"] for item in self._cart)
