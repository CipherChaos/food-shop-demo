import pytest

class TestCartManager:
    def test_add_new_item(self, cart):
        cart.add("زرشک پلو", 170000)
        assert len(cart.cart()) == 1
        assert cart.cart()[0] == {"name": "زرشک پلو", "price": 170000, "qty": 1}

    def test_add_existing_item_increments_qty(self, cart):
        cart.add("کباب", 160000)
        cart.add("کباب", 160000)
        assert len(cart.cart()) == 1
        assert cart.cart()[0]["qty"] == 2

    def test_decrement_reduces_qty(self, cart):
        cart.add("دوغ", 15000)
        cart.add("دوغ", 15000)
        cart.decrement("دوغ")
        assert cart.quantity("دوغ") == 1

    def test_decrement_removes_when_qty_one(self, cart):
        cart.add("دوغ", 15000)
        cart.decrement("دوغ")
        assert len(cart.cart()) == 0

    def test_remove(self, cart):
        cart.add("سالاد", 50000)
        cart.remove("سالاد")
        assert len(cart.cart()) == 0

    def test_clear(self, cart):
        cart.add("آب", 10000)
        cart.add("آب", 10000)
        cart.clear()
        assert len(cart.cart()) == 0

    def test_total_price(self, cart):
        cart.add("کباب", 160000)
        cart.add("دوغ", 15000)
        assert cart.total_price() == 175000

    def test_item_added_signal(self, qtbot, cart):
        with qtbot.waitSignal(cart.item_added, timeout=1000) as blocker:
            cart.add("پیتزا", 120000)
        assert "پیتزا" in blocker.args[0]

    def test_cart_changed_signal_on_add(self, qtbot, cart):
        with qtbot.waitSignal(cart.cart_changed, timeout=1000):
            cart.add("برگر", 90000)

    def test_cart_changed_signal_on_decrement(self, qtbot, cart):
        cart.add("برگر", 90000)
        with qtbot.waitSignal(cart.cart_changed, timeout=1000):
            cart.decrement("برگر")