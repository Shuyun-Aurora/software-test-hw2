import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

USERNAME = "standard_user"
PASSWORD = "secret_sauce"


@pytest.mark.tc01
def test_tc01_login_enters_inventory_page(driver, base_url):
    login_page = LoginPage(driver, base_url=base_url)
    inventory_page = InventoryPage(driver)

    login_page.open()

    assert login_page.login_form_is_visible()
    assert login_page.username_input_is_visible()
    assert login_page.password_input_is_visible()
    assert login_page.login_button_is_clickable()

    login_page.login(USERNAME, PASSWORD)
    inventory_page.wait_until_loaded()

    assert "/inventory.html" in driver.current_url
    assert inventory_page.title_text() == "Products"
    assert inventory_page.item_count() == 6
    assert len(inventory_page.item_names()) == 6
    assert inventory_page.sort_select_is_visible()
    assert inventory_page.cart_is_visible()
