import pytest


EXPECTED_SORT_OPTIONS = [
    "Name (A to Z)",
    "Name (Z to A)",
    "Price (low to high)",
    "Price (high to low)",
]


@pytest.mark.tc02
def test_tc02_product_sorting_options_and_results(logged_in_inventory):
    inventory_page = logged_in_inventory

    assert inventory_page.sort_select_is_visible()
    assert inventory_page.sort_options() == EXPECTED_SORT_OPTIONS

    inventory_page.sort_by_visible_text("Name (Z to A)")
    names_desc = inventory_page.item_names()
    assert names_desc == sorted(names_desc, reverse=True)

    inventory_page.sort_by_visible_text("Name (A to Z)")
    names_asc = inventory_page.item_names()
    assert names_asc == sorted(names_asc)

    inventory_page.sort_by_visible_text("Price (low to high)")
    prices_asc = inventory_page.item_prices()
    assert prices_asc == sorted(prices_asc)

    inventory_page.sort_by_visible_text("Price (high to low)")
    prices_desc = inventory_page.item_prices()
    assert prices_desc == sorted(prices_desc, reverse=True)
