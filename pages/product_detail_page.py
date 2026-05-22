from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProductDetailPage:
    PATH_FRAGMENT = "/inventory-item.html"

    PRODUCT_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_IMAGE = (By.CLASS_NAME, "inventory_details_img")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    BACK_BUTTON = (By.ID, "back-to-products")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.url_contains(self.PATH_FRAGMENT))
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_NAME))

    def product_name(self) -> str:
        self.wait_until_loaded()
        return self.driver.find_element(*self.PRODUCT_NAME).text

    def product_description(self) -> str:
        self.wait_until_loaded()
        return self.driver.find_element(*self.PRODUCT_DESCRIPTION).text

    def product_price(self) -> Decimal:
        self.wait_until_loaded()
        price_text = self.driver.find_element(*self.PRODUCT_PRICE).text
        return Decimal(price_text.replace("$", ""))

    def product_image_is_visible(self) -> bool:
        image = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_IMAGE))
        return image.is_displayed()

    def add_to_cart_button_is_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON)
        ).is_displayed()

    def add_to_cart(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.REMOVE_BUTTON))

    def remove_button_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.REMOVE_BUTTON)).text

    def cart_badge_count(self) -> int:
        badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        return int(badge.text)

    def back_to_products(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.BACK_BUTTON)).click()
