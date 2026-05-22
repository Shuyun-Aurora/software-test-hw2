import pytest

from pages.product_detail_page import ProductDetailPage


PRODUCT_NAME = "Sauce Labs Backpack"
SECOND_PRODUCT_NAME = "Sauce Labs Bike Light"


@pytest.mark.tc04
def test_tc04_add_products_to_cart_updates_button_and_badge(logged_in_inventory):
    inventory_page = logged_in_inventory
    detail_page = ProductDetailPage(inventory_page.driver)

    inventory_page.add_product_to_cart(PRODUCT_NAME)

    assert inventory_page.remove_button_text_by_name(PRODUCT_NAME) == "Remove"
    assert inventory_page.cart_badge_count() == 1

    inventory_page.open_product_detail(SECOND_PRODUCT_NAME)
    detail_page.wait_until_loaded()
    detail_page.add_to_cart()

    assert detail_page.remove_button_text() == "Remove"
    assert detail_page.cart_badge_count() == 2
