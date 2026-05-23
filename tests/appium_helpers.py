from appium import webdriver
from appium.options.android import UiAutomator2Options


APPIUM_SERVER_URL = "http://127.0.0.1:4723"
SAUCEDEMO_URL = "https://www.saucedemo.com/"
SAUCEDEMO_USERNAME = "standard_user"
SAUCEDEMO_PASSWORD = "secret_sauce"


def create_android_chrome_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.device_name = "Android Emulator"
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:chromedriverAutodownload", True)

    return webdriver.Remote(APPIUM_SERVER_URL, options=options)
