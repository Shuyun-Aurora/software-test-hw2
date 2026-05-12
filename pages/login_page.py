from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    LOGIN_FORM = (By.CSS_SELECTOR, "form")

    def __init__(
        self,
        driver: WebDriver,
        base_url: str = "https://www.saucedemo.com/",
        timeout: int = 10,
    ):
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))

    def login(self, username: str, password: str) -> None:
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
