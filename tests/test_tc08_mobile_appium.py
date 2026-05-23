import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from tests.appium_helpers import (
    SAUCEDEMO_PASSWORD,
    SAUCEDEMO_URL,
    SAUCEDEMO_USERNAME,
    create_android_chrome_driver,
)


@pytest.mark.tc08
def test_tc08_mobile_appium_core_shopping_flow():
    driver = create_android_chrome_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(SAUCEDEMO_URL)

        username_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-button"))
        )

        assert username_input.is_displayed()
        assert password_input.is_displayed()
        assert login_button.is_enabled()

        username_input.clear()
        username_input.send_keys(SAUCEDEMO_USERNAME)
        password_input.clear()
        password_input.send_keys(SAUCEDEMO_PASSWORD)
        login_button.click()

        wait.until(EC.url_contains("/inventory.html"))
        title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
        inventory_items = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item"))
        )
        cart_link = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_link"))
        )

        assert title.text == "Products"
        assert len(inventory_items) >= 1
        assert cart_link.is_displayed()

        sort_select = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".product_sort_container")
            )
        )
        Select(sort_select).select_by_visible_text("Price (low to high)")
        prices = [
            float(price.text.replace("$", ""))
            for price in driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        ]
        assert prices == sorted(prices)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait.until(
            lambda current_driver: current_driver.execute_script("return window.scrollY")
            > 0
        )

        driver.execute_script("window.scrollTo(0, 0);")
        product_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#item_4_title_link"))
        )
        click_element(driver, product_link)

        wait.until(EC.url_contains("/inventory-item.html"))
        detail_title = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".inventory_details_name")
            )
        )
        detail_price = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".inventory_details_price")
            )
        )

        assert detail_title.text == "Sauce Labs Backpack"
        assert detail_price.text == "$29.99"

        back_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#back-to-products"))
        )
        click_element(driver, back_button)
        wait.until(EC.url_contains("/inventory.html"))

        add_to_cart_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#add-to-cart-sauce-labs-backpack")
            )
        )
        click_element(driver, add_to_cart_button)

        remove_button = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#remove-sauce-labs-backpack")
            )
        )
        cart_badge = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge"))
        )

        assert remove_button.text == "Remove"
        assert cart_badge.text == "1"

        cart_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".shopping_cart_link"))
        )
        click_element(driver, cart_link)
        wait.until(EC.url_contains("/cart.html"))
        cart_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
        )
        cart_item_name = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item_name"))
        )
        cart_quantity = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart_quantity"))
        )

        assert cart_title.text == "Your Cart"
        assert cart_item_name.text == "Sauce Labs Backpack"
        assert cart_quantity.text == "1"

        checkout_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkout"))
        )
        click_element(driver, checkout_button)

        wait.until(EC.url_contains("/checkout-step-one.html"))
        first_name_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#first-name"))
        )
        last_name_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#last-name"))
        )
        postal_code_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#postal-code"))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", first_name_input
        )
        first_name_input.send_keys("Mobile")
        last_name_input.send_keys("User")
        postal_code_input.send_keys("100000")

        continue_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#continue"))
        )
        click_element(driver, continue_button)

        wait.until(EC.url_contains("/checkout-step-two.html"))
        overview_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
        )
        overview_item_name = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item_name"))
        )

        assert overview_title.text == "Checkout: Overview"
        assert overview_item_name.text == "Sauce Labs Backpack"

        finish_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#finish"))
        )
        click_element(driver, finish_button)

        wait.until(EC.url_contains("/checkout-complete.html"))
        complete_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
        )
        complete_header = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".complete-header"))
        )

        assert complete_title.text == "Checkout: Complete!"
        assert complete_header.text == "Thank you for your order!"
    finally:
        driver.quit()


def click_element(driver, element) -> None:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)
