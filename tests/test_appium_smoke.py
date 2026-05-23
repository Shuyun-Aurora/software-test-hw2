from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.appium_helpers import SAUCEDEMO_URL, create_android_chrome_driver


def test_open_saucedemo_in_android_chrome():
    driver = create_android_chrome_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(SAUCEDEMO_URL)

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login-button")))
        assert "Swag Labs" in driver.title
    finally:
        driver.quit()
