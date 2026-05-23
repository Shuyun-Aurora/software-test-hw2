import pytest


@pytest.mark.tc07
def test_tc07_sidebar_navigation_menu_opens_shows_links_and_closes(
    logged_in_inventory,
):
    inventory_page = logged_in_inventory

    assert inventory_page.sidebar_menu_button_is_visible()

    inventory_page.open_sidebar()

    assert inventory_page.sidebar_close_button_is_visible()
    assert inventory_page.sidebar_link_texts() == [
        "All Items",
        "About",
        "Logout",
        "Reset App State",
    ]

    inventory_page.close_sidebar()

    assert inventory_page.sidebar_is_hidden()
