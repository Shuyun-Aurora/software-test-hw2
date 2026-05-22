import pytest

from pages.cart_page import CartPage


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.tc05
def test_tc05_cart_page_displays_added_product_information(logged_in_inventory):
    inventory_page = logged_in_inventory
    expected_description = inventory_page.item_description_by_name(PRODUCT_NAME)
    expected_price = inventory_page.item_price_by_name(PRODUCT_NAME)
    cart_page = CartPage(inventory_page.driver)

    inventory_page.add_product_to_cart(PRODUCT_NAME)
    assert inventory_page.cart_badge_count() == 1

    inventory_page.open_cart()
    cart_page.wait_until_loaded()

    assert cart_page.title_text() == "Your Cart"
    assert cart_page.item_count() == 1
    assert PRODUCT_NAME in cart_page.item_names()
    assert cart_page.item_quantity_by_name(PRODUCT_NAME) == 1
    assert cart_page.item_description_by_name(PRODUCT_NAME) == expected_description
    assert cart_page.item_price_by_name(PRODUCT_NAME) == expected_price
    assert cart_page.continue_shopping_is_visible()
    assert cart_page.checkout_is_visible()
