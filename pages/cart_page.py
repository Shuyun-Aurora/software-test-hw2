from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    PATH_FRAGMENT = "/cart.html"

    TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.TITLE))

    def title_text(self) -> str:
        self.wait_until_loaded()
        return self.driver.find_element(*self.TITLE).text

    def item_count(self) -> int:
        self.wait_until_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def item_names(self) -> list[str]:
        return [
            item.find_element(By.CLASS_NAME, "inventory_item_name").text
            for item in self._cart_items()
        ]

    def item_quantity_by_name(self, product_name: str) -> int:
        quantity_text = self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "cart_quantity"
        ).text
        return int(quantity_text)

    def item_description_by_name(self, product_name: str) -> str:
        return self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_desc"
        ).text

    def item_price_by_name(self, product_name: str) -> Decimal:
        price_text = self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text
        return Decimal(price_text.replace("$", ""))

    def continue_shopping_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.CONTINUE_SHOPPING_BUTTON)
        ).is_displayed()

    def checkout_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.CHECKOUT_BUTTON)
        ).is_displayed()

    def _cart_items(self):
        self.wait_until_loaded()
        return self.driver.find_elements(*self.CART_ITEMS)

    def _item_by_name(self, product_name: str):
        for item in self._cart_items():
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                return item
        raise AssertionError(f"Product not found on cart page: {product_name}")
