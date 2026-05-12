import pytest


@pytest.mark.tc01
def test_tc01_login_enters_inventory_page(logged_in_inventory, driver):
    inventory_page = logged_in_inventory

    assert "/inventory.html" in driver.current_url
    assert inventory_page.title_text() == "Products"
    assert len(inventory_page.item_names()) > 0
    assert inventory_page.cart_is_visible()

