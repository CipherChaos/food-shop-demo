import pytest
from app.core.cart_manager import CartManager
from app.ui.menu_section import MenuSection

class TestMenuSection:
    @pytest.fixture
    def section(self, qapp, cart):
        return MenuSection(cart)

    def test_initial_category_selected(self, section):
        assert section.category_buttons[0].isChecked()

    def test_switch_category(self, qtbot, section):
        section.category_buttons[2].click()
        qtbot.wait(100)
        assert section.current_category == "Nooshidani"

    def test_search_filters_items(self, section, qtbot):
        section.search_bar.setText("سالاد")
        qtbot.wait(200)
        cards = list(section.item_cards.values())
        assert all("سالاد" in card.persian_name for card in cards)

    def test_clear_search_shows_all(self, section, qtbot):
        section.search_bar.setText("سالاد")
        qtbot.wait(100)
        section.search_bar.setText("")
        qtbot.wait(100)
        assert len(section.item_cards) == 5

    def test_add_item_signal_emitted(self, qtbot, section):
        first_card = list(section.item_cards.values())[0]
        with qtbot.waitSignal(section.add_item, timeout=500) as blocker:
            first_card.add_clicked.emit(first_card.persian_name, first_card.price)
        assert blocker.args[0] == first_card.persian_name