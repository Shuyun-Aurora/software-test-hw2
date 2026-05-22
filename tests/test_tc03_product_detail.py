import pytest

from pages.product_detail_page import ProductDetailPage


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.tc03
def test_tc03_product_detail_page_shows_product_information(logged_in_inventory):
    inventory_page = logged_in_inventory
    expected_description = inventory_page.item_description_by_name(PRODUCT_NAME)
    expected_price = inventory_page.item_price_by_name(PRODUCT_NAME)
    detail_page = ProductDetailPage(inventory_page.driver)

    inventory_page.open_product_detail(PRODUCT_NAME)
    detail_page.wait_until_loaded()

    assert "/inventory-item.html" in inventory_page.driver.current_url
    assert detail_page.product_name() == PRODUCT_NAME
    assert detail_page.product_description() == expected_description
    assert detail_page.product_price() == expected_price
    assert detail_page.product_image_is_visible()
    assert detail_page.add_to_cart_button_is_visible()

    detail_page.back_to_products()
    inventory_page.wait_until_loaded()
    assert inventory_page.title_text() == "Products"
