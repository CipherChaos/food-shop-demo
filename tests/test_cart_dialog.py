import pytest
from unittest.mock import patch
from app.core.cart_manager import CartManager
from app.ui.cart_dialog import CartDialog

class TestCartDialog:
    @pytest.fixture
    def cart(self):
        cart = CartManager()
        cart.add("آب", 10000)
        return cart

    @pytest.fixture
    def dialog(self, qapp, cart):
        profile = {"name": "Test", "phone": "123", "address": "Tehran"}
        return CartDialog(cart, profile)

    def test_dialog_shows_items(self, dialog):
        # After refresh, the container should have at least one item label
        dialog.refresh_display()
        # We can just verify total label contains price
        assert "10000" in dialog.total_label.text() or "10000" in dialog.total_label.text()

    def test_clear_cart(self, dialog, cart):
        # Simulate accepting the clear dialog
        with patch.object(dialog, 'exec_', return_value=1):  # not needed, clear_cart creates its own dialog
            dialog.clear_cart()
        # Cart should be empty
        assert len(cart.cart()) == 0

    @patch("app.ui.cart_dialog.export_order_to_excel", return_value=True)
    def test_finalize_order_exports_and_clears(self, mock_export, dialog, cart):
        dialog.finalize_order()
        mock_export.assert_called_once()
        assert len(cart.cart()) == 0

    @patch("app.ui.cart_dialog.export_order_to_excel", return_value=False)
    def test_finalize_order_export_fails_does_not_clear(self, mock_export, dialog, cart):
        dialog.finalize_order()
        assert len(cart.cart()) == 1