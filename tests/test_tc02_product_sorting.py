import pytest


@pytest.mark.tc02
def test_tc02_sort_products_by_name_descending(logged_in_inventory):
    inventory_page = logged_in_inventory

    inventory_page.sort_by_visible_text("Name (Z to A)")
    names = inventory_page.item_names()

    assert names == sorted(names, reverse=True)


@pytest.mark.tc02
def test_tc02_sort_products_by_price_low_to_high(logged_in_inventory):
    inventory_page = logged_in_inventory

    inventory_page.sort_by_visible_text("Price (low to high)")
    prices = inventory_page.item_prices()

    assert prices == sorted(prices)

