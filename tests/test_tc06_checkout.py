import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.tc06
def test_tc06_checkout_completes_order(logged_in_inventory):
    inventory_page = logged_in_inventory
    expected_price = inventory_page.item_price_by_name(PRODUCT_NAME)
    cart_page = CartPage(inventory_page.driver)
    checkout_page = CheckoutPage(inventory_page.driver)

    inventory_page.add_product_to_cart(PRODUCT_NAME)
    inventory_page.open_cart()
    cart_page.wait_until_loaded()
    cart_page.checkout()

    checkout_page.wait_until_information_loaded()
    assert checkout_page.title_text() == "Checkout: Your Information"
    assert checkout_page.checkout_form_is_visible()
    assert checkout_page.first_name_input_is_visible()
    assert checkout_page.last_name_input_is_visible()
    assert checkout_page.postal_code_input_is_visible()

    checkout_page.fill_customer_information("Test", "User", "100000")
    checkout_page.continue_to_overview()

    checkout_page.wait_until_overview_loaded()
    assert checkout_page.title_text() == "Checkout: Overview"
    assert checkout_page.item_count() == 1
    assert PRODUCT_NAME in checkout_page.item_names()
    assert checkout_page.item_price_by_name(PRODUCT_NAME) == expected_price
    assert checkout_page.finish_is_visible()

    checkout_page.finish_order()

    checkout_page.wait_until_complete_loaded()
    assert checkout_page.title_text() == "Checkout: Complete!"
    assert checkout_page.complete_header_text() == "Thank you for your order!"
    assert "Your order has been dispatched" in checkout_page.complete_text()
    assert checkout_page.back_home_is_visible()
