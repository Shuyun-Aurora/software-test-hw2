from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class InventoryPage:
    PATH_FRAGMENT = "/inventory.html"

    TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_NAMES = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        self.wait.until(EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS))

    def title_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def item_names(self) -> list[str]:
        self.wait_until_loaded()
        return [element.text for element in self.driver.find_elements(*self.INVENTORY_NAMES)]

    def item_count(self) -> int:
        self.wait_until_loaded()
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def item_prices(self) -> list[Decimal]:
        self.wait_until_loaded()
        prices = []
        for element in self.driver.find_elements(*self.INVENTORY_PRICES):
            prices.append(Decimal(element.text.replace("$", "")))
        return prices

    def item_description_by_name(self, product_name: str) -> str:
        return self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_desc"
        ).text

    def item_price_by_name(self, product_name: str) -> Decimal:
        price_text = self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text
        return Decimal(price_text.replace("$", ""))

    def sort_select_is_visible(self) -> bool:
        return self.wait.until(EC.visibility_of_element_located(self.SORT_SELECT)).is_displayed()

    def sort_options(self) -> list[str]:
        select_element = self.wait.until(EC.visibility_of_element_located(self.SORT_SELECT))
        return [option.text for option in Select(select_element).options]

    def cart_is_visible(self) -> bool:
        return self.wait.until(EC.visibility_of_element_located(self.CART_LINK)).is_displayed()

    def cart_badge_count(self) -> int:
        badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        return int(badge.text)

    def sort_by_visible_text(self, visible_text: str) -> None:
        select_element = self.wait.until(EC.element_to_be_clickable(self.SORT_SELECT))
        Select(select_element).select_by_visible_text(visible_text)
        self.wait.until(lambda _: self.item_names())

    def open_product_detail(self, product_name: str) -> None:
        self._item_by_name(product_name).find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).click()

    def add_product_to_cart(self, product_name: str) -> None:
        item = self._item_by_name(product_name)
        item.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart']").click()
        self.wait.until(
            lambda _: item.find_element(By.CSS_SELECTOR, "button").text == "Remove"
        )

    def remove_button_text_by_name(self, product_name: str) -> str:
        return self._item_by_name(product_name).find_element(By.CSS_SELECTOR, "button").text

    def open_cart(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()

    def _item_by_name(self, product_name: str):
        self.wait_until_loaded()
        for item in self.driver.find_elements(*self.INVENTORY_ITEMS):
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                return item
        raise AssertionError(f"Product not found on inventory page: {product_name}")
