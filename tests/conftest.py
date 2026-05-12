from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


SCREENSHOT_DIR = Path("artifacts/screenshots")
SAUCEDEMO_USERNAME = "standard_user"
SAUCEDEMO_PASSWORD = "secret_sauce"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode.",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="SauceDemo base URL.",
    )


@pytest.fixture
def base_url(request) -> str:
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=0")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)

    yield browser

    browser.quit()


@pytest.fixture
def logged_in_inventory(driver, base_url):
    login_page = LoginPage(driver, base_url=base_url)
    inventory_page = InventoryPage(driver)

    login_page.open()
    login_page.login(SAUCEDEMO_USERNAME, SAUCEDEMO_PASSWORD)
    inventory_page.wait_until_loaded()

    return inventory_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
    browser.save_screenshot(str(screenshot_path))
