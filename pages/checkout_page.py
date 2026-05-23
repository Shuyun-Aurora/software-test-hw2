from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:
    INFORMATION_PATH_FRAGMENT = "/checkout-step-one.html"
    OVERVIEW_PATH_FRAGMENT = "/checkout-step-two.html"
    COMPLETE_PATH_FRAGMENT = "/checkout-complete.html"

    TITLE = (By.CLASS_NAME, "title")
    CHECKOUT_FORM = (By.CSS_SELECTOR, ".checkout_info")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_information_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.INFORMATION_PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_FORM))

    def wait_until_overview_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.OVERVIEW_PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        self.wait.until(EC.visibility_of_all_elements_located(self.CART_ITEMS))

    def wait_until_complete_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.COMPLETE_PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER))

    def title_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def checkout_form_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.CHECKOUT_FORM)
        ).is_displayed()

    def first_name_input_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        ).is_displayed()

    def last_name_input_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        ).is_displayed()

    def postal_code_input_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.POSTAL_CODE_INPUT)
        ).is_displayed()

    def fill_customer_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        self.wait_until_information_loaded()
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)

    def continue_to_overview(self) -> None:
        self._click_button(self.CONTINUE_BUTTON)

    def finish_order(self) -> None:
        self._click_button(self.FINISH_BUTTON)

    def item_count(self) -> int:
        self.wait_until_overview_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def item_names(self) -> list[str]:
        return [
            item.find_element(By.CLASS_NAME, "inventory_item_name").text
            for item in self._cart_items()
        ]

    def item_price_by_name(self, product_name: str) -> Decimal:
        price_text = self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text
        return Decimal(price_text.replace("$", ""))

    def finish_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.FINISH_BUTTON)
        ).is_displayed()

    def complete_header_text(self) -> str:
        self.wait_until_complete_loaded()
        return self.driver.find_element(*self.COMPLETE_HEADER).text

    def complete_text(self) -> str:
        self.wait_until_complete_loaded()
        return self.driver.find_element(*self.COMPLETE_TEXT).text

    def back_home_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.BACK_HOME_BUTTON)
        ).is_displayed()

    def _cart_items(self):
        self.wait_until_overview_loaded()
        return self.driver.find_elements(*self.CART_ITEMS)

    def _item_by_name(self, product_name: str):
        for item in self._cart_items():
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                return item
        raise AssertionError(f"Product not found on checkout overview: {product_name}")

    def _click_button(self, locator: tuple[str, str]) -> None:
        button = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        button.click()
