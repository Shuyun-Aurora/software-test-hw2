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

    def item_prices(self) -> list[Decimal]:
        self.wait_until_loaded()
        prices = []
        for element in self.driver.find_elements(*self.INVENTORY_PRICES):
            prices.append(Decimal(element.text.replace("$", "")))
        return prices

    def cart_is_visible(self) -> bool:
        return self.wait.until(EC.visibility_of_element_located(self.CART_LINK)).is_displayed()

    def sort_by_visible_text(self, visible_text: str) -> None:
        select_element = self.wait.until(EC.element_to_be_clickable(self.SORT_SELECT))
        Select(select_element).select_by_visible_text(visible_text)
        self.wait.until(lambda _: self.item_names())
