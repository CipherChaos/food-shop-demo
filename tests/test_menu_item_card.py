from app.ui.menu_item_card import MenuItemCard

class TestMenuItemCard:
    def test_initial_state_shows_add_button(self, qapp):
        card = MenuItemCard("کباب", 160000, initial_qty=0)
        assert card.add_btn.isVisible()
        assert not card.counter_widget.isVisible()

    def test_positive_qty_shows_counter(self, qapp):
        card = MenuItemCard("کباب", 160000, initial_qty=2)
        card.update_display(2)
        assert not card.add_btn.isVisible()
        assert card.counter_widget.isVisible()

    def test_add_clicked_emits_signal(self, qtbot):
        card = MenuItemCard("کباب", 160000)
        with qtbot.waitSignal(card.add_clicked, timeout=500) as blocker:
            card.add_btn.click()
        assert blocker.args == ("کباب", 160000)

    def test_decrement_clicked_emits_signal(self, qtbot):
        card = MenuItemCard("کباب", 160000, initial_qty=1)
        with qtbot.waitSignal(card.decrement_clicked, timeout=500) as blocker:
            card.minus_btn.click()
        assert blocker.args == ("کباب",)