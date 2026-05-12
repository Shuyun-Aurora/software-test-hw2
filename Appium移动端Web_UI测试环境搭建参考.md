# Appium 移动端 Web UI 测试环境搭建参考

> 适用场景：Windows 10/11 电脑上，使用 **Appium + Android 模拟器 + Chrome 浏览器** 对 SauceDemo 等 Web 网站进行移动端 UI 自动化测试。  
> 建议定位：作为 GUI 测试作业的移动端加分项，不替代桌面端 Selenium 主体测试。

---

## 1. 最终要搭起来的测试链路

```text
pytest 测试脚本
    ↓
Appium-Python-Client
    ↓
Appium Server
    ↓
UiAutomator2 Driver
    ↓
Android Emulator
    ↓
模拟器中的 Chrome 浏览器
    ↓
SauceDemo 网站
```

也就是说，Python 测试脚本不是直接操作 Chrome，而是先连接 Appium Server，再由 Appium 调用 Android 模拟器中的 Chrome 浏览器完成移动端 Web UI 测试。

---

## 2. 需要安装的软件

需要提前安装这些工具：

```text
1. Android Studio
2. Android SDK Platform-Tools
3. Android Emulator
4. Android 模拟器，例如 Pixel 5 / Pixel 6
5. Node.js
6. Appium
7. Appium UiAutomator2 Driver
8. Python
9. pytest、selenium、Appium-Python-Client
```

推荐使用 Android 模拟器，不推荐一开始就用 iOS，因为 iOS 自动化通常依赖 macOS 和 Xcode，Windows 上不方便。

---

## 3. 安装 Android Studio 和 SDK

先安装 Android Studio，安装时基本保持默认选项即可。

安装完成后，打开 Android Studio，进入：

```text
File / Settings
→ Languages & Frameworks
→ Android SDK
```

确认安装以下组件：

```text
Android SDK Platform-Tools
Android SDK Build-Tools
Android Emulator
Android SDK Platform，例如 Android 13 或 Android 14
```

其中：

- `Platform-Tools` 提供 `adb` 命令；
- `Android Emulator` 用于启动 Android 模拟器；
- `Android SDK Platform` 是模拟器运行所需的 Android 系统平台。

---

## 4. 创建 Android 模拟器

在 Android Studio 中打开：

```text
Tools
→ Device Manager
→ Create Device
```

推荐选择：

```text
Pixel 5 或 Pixel 6
Android 13 / Android 14
Google APIs 或 Google Play 镜像
```

建议选择带 `Google APIs` 或 `Google Play` 的镜像，因为后续需要模拟器中有 Chrome 浏览器。

创建完成后，在 Device Manager 中点击启动按钮，启动模拟器。

启动后检查模拟器里是否有 Chrome 浏览器。如果没有 Chrome，可以换一个带 Google Play 的系统镜像重新创建模拟器。

---

## 5. 配置 Windows 环境变量

Android SDK 默认路径一般是：

```text
C:\Users\你的用户名\AppData\Local\Android\Sdk
```

打开 Windows 环境变量设置：

```text
此电脑
→ 属性
→ 高级系统设置
→ 环境变量
```

新建用户变量或系统变量：

```text
变量名：ANDROID_HOME
变量值：C:\Users\你的用户名\AppData\Local\Android\Sdk
```

然后在 `Path` 中加入以下两项：

```text
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\emulator
```

保存后，重新打开一个 PowerShell，执行：

```powershell
adb version
```

如果能看到 adb 版本号，说明环境变量配置成功。

---

## 6. 检查 adb 是否能识别模拟器

先确保 Android 模拟器已经启动。

然后在 PowerShell 中执行：

```powershell
adb devices
```

正常结果类似：

```text
List of devices attached
emulator-5554    device
```

这一步非常关键。

如果看不到 `emulator-5554 device`，后面的 Appium 测试一定跑不起来。需要先检查：

```text
1. Android 模拟器是否已经启动；
2. ANDROID_HOME 是否配置正确；
3. Path 是否包含 %ANDROID_HOME%\platform-tools；
4. PowerShell 是否是在配置环境变量之后重新打开的。
```

---

## 7. 安装 Node.js

Appium 是通过 npm 安装的，所以需要先安装 Node.js。

建议安装 Node.js LTS 版本。

安装完成后，重新打开 PowerShell，执行：

```powershell
node -v
npm -v
```

如果能正常输出版本号，说明 Node.js 和 npm 安装成功。

---

## 8. 安装 Appium 和 UiAutomator2 Driver

在 PowerShell 中执行：

```powershell
npm install -g appium
```

检查 Appium 是否安装成功：

```powershell
appium -v
```

然后安装 Android 自动化驱动：

```powershell
appium driver install uiautomator2
```

检查已安装的 Appium 驱动：

```powershell
appium driver list --installed
```

正常情况下，应能看到 `uiautomator2`。

再执行环境检查：

```powershell
appium driver doctor uiautomator2
```

如果 required 项没有报错，基本可以继续。warning 可以先记录，不一定马上处理。

---

## 9. 启动 Appium Server

新开一个 PowerShell 窗口，执行：

```powershell
appium
```

正常情况下，会看到类似信息：

```text
Appium REST http interface listener started on http://0.0.0.0:4723
```

或类似的 4723 端口监听信息。

这个 PowerShell 窗口不要关闭。后续 Python 测试脚本会连接：

```text
http://127.0.0.1:4723
```

如果这个窗口关闭，测试脚本会连接失败。

---

## 10. 准备 Python 测试环境

进入测试项目目录，例如：

```powershell
cd D:\saucedemo-gui-test
```

创建虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\activate
```

安装 Python 依赖：

```powershell
pip install pytest selenium Appium-Python-Client
```

---

## 11. 建议项目目录结构

可以按下面方式组织项目：

```text
saucedemo-gui-test/
├─ tests/
│  ├─ test_appium_smoke.py
│  └─ test_tc08_mobile.py
├─ screenshots/
├─ requirements.txt
└─ README.md
```

如果没有 `screenshots` 文件夹，需要手动创建：

```powershell
mkdir screenshots
```

也可以把依赖写入 `requirements.txt`：

```text
pytest
selenium
Appium-Python-Client
```

以后别人可以直接执行：

```powershell
pip install -r requirements.txt
```

---

## 12. 先跑最小冒烟测试

不要一开始就写完整测试用例。先确认 Appium 能打开 Android 模拟器中的 Chrome，并访问 SauceDemo。

新建文件：

```text
tests/test_appium_smoke.py
```

内容如下：

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_open_saucedemo_in_android_chrome():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.device_name = "Android Emulator"

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    try:
        driver.get("https://www.saucedemo.com/")
        assert "Swag Labs" in driver.title
    finally:
        driver.quit()
```

运行：

```powershell
pytest tests/test_appium_smoke.py -v
```

如果该测试通过，说明移动端 Web UI 自动化环境已经基本搭建成功。

---

## 13. TC08：移动端 Web UI 关键交互抽测

该用例建议作为作业中的移动端加分项，不需要重复桌面端完整结算流程。

测试目标：

```text
验证 SauceDemo 在 Android Chrome 移动端浏览器环境下，登录、商品列表展示、滑动浏览、加购和购物车跳转是否正常。
```

新建文件：

```text
tests/test_tc08_mobile.py
```

内容如下：

```python
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_mobile_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.device_name = "Android Emulator"

    return webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )


def test_tc08_mobile_web_key_interaction():
    driver = create_mobile_driver()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "user-name"))
        ).send_keys("standard_user")

        driver.find_element(AppiumBy.ID, "password").send_keys("secret_sauce")
        driver.find_element(AppiumBy.ID, "login-button").click()

        wait.until(
            EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "inventory_list"))
        )

        assert driver.find_element(AppiumBy.CLASS_NAME, "inventory_list").is_displayed()

        # 模拟移动端上滑，浏览商品列表
        driver.swipe(500, 1400, 500, 500, 800)
        time.sleep(1)

        add_buttons = driver.find_elements(
            AppiumBy.XPATH,
            "//button[contains(text(), 'Add to cart')]"
        )

        assert len(add_buttons) > 0
        add_buttons[0].click()

        badge = wait.until(
            EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "shopping_cart_badge"))
        )
        assert badge.text == "1"

        driver.find_element(AppiumBy.CLASS_NAME, "shopping_cart_link").click()

        wait.until(
            EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "cart_list"))
        )

        assert "cart" in driver.current_url

        driver.save_screenshot("screenshots/tc08_mobile_cart.png")

    finally:
        driver.quit()
```

运行：

```powershell
pytest tests/test_tc08_mobile.py -v
```

如果运行成功，会在 `screenshots` 目录下生成截图：

```text
screenshots/tc08_mobile_cart.png
```

---

## 14. 如果 swipe 不稳定怎么办

有些 Appium 版本或 WebView 场景下，`driver.swipe()` 可能不稳定。

可以临时替换为 JavaScript 滚动：

```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

不过，如果报告里想突出移动端触控/手势，优先保留 `swipe()`。如果确实不稳定，可以在报告中说明：

```text
移动端页面滑动操作在 Appium 环境下存在兼容性差异，测试中使用 JavaScript 滚动作为补充验证方式。
```

---

## 15. 常见问题排查

### 15.1 adb devices 看不到 emulator-5554

可能原因：

```text
1. Android 模拟器没有启动；
2. ANDROID_HOME 配置错误；
3. Path 没有加入 %ANDROID_HOME%\platform-tools；
4. 配置环境变量后没有重新打开 PowerShell。
```

解决方式：

```powershell
adb version
adb devices
```

先确保 adb 可用，再确认模拟器已启动。

---

### 15.2 appium driver list --installed 没有 uiautomator2

说明 Appium Android 驱动没有安装。

执行：

```powershell
appium driver install uiautomator2
appium driver list --installed
```

---

### 15.3 pytest 连接不上 127.0.0.1:4723

一般是 Appium Server 没启动。

新开 PowerShell 执行：

```powershell
appium
```

保持该窗口不要关闭，然后再运行 pytest。

---

### 15.4 模拟器里没有 Chrome

可能是创建模拟器时选择了不带 Google 服务的镜像。

建议重新创建模拟器，选择：

```text
Google APIs 或 Google Play 镜像
```

---

### 15.5 ChromeDriver 版本不兼容

这是 Appium 移动端 Web 测试中比较常见的问题。

表现可能包括：

```text
session not created
chromedriver version mismatch
cannot automate Chrome
```

处理建议：

```text
1. 先保存报错截图，作为环境问题记录；
2. 尝试更新 Appium 和 uiautomator2 driver；
3. 尝试换一个 Android 模拟器系统版本；
4. 如果仍无法解决，可使用 Chrome mobile emulation 作为补充验证。
```

---

## 16. 推荐执行顺序

实际操作时，建议严格按下面顺序验证：

```text
1. 启动 Android 模拟器
2. 执行 adb devices
3. 确认看到 emulator-5554 device
4. 执行 appium driver list --installed
5. 确认存在 uiautomator2
6. 执行 appium driver doctor uiautomator2
7. 新开窗口执行 appium，启动 Appium Server
8. 执行 pytest tests/test_appium_smoke.py -v
9. 冒烟测试通过后，再执行 pytest tests/test_tc08_mobile.py -v
```

不要跳过冒烟测试。冒烟测试不通过时，不要急着写完整测试用例。

---

## 17. 报告中可以这样描述

可以在测试计划或测试报告中写：

```text
除桌面端 Selenium Web 自动化测试外，本项目额外设计了移动端 Web UI 关键交互抽测。移动端测试环境采用 Appium + Android Emulator + Chrome，由 Appium Server 通过 UiAutomator2 Driver 驱动 Android 模拟器中的 Chrome 浏览器访问 SauceDemo 网站。该用例重点验证移动端浏览器环境下登录、商品列表展示、页面滑动、触控点击、购物车 badge 更新和购物车页面跳转等关键交互，不重复执行桌面端已完整覆盖的结算流程。
```

也可以补充风险说明：

```text
由于 Appium 移动端测试环境依赖 Android SDK、模拟器、Chrome 与自动化驱动版本，环境搭建复杂度高于桌面端 Selenium。因此本项目将移动端 Appium 测试作为补充抽测与加分模块，桌面端 Selenium 用例仍作为主要功能覆盖依据。若 Appium 环境受限，则使用 Chrome mobile emulation 作为移动端响应式布局的补充验证。
```

---

## 18. 本环境搭建的最低成功标准

如果下面三项都通过，就可以认为移动端 Web UI 测试环境基本搭建完成：

```text
1. adb devices 能看到 emulator-5554 device；
2. Appium Server 能在 4723 端口正常启动；
3. test_appium_smoke.py 能打开 Android Chrome 并访问 SauceDemo。
```

在此基础上，再执行 TC08 移动端 Web UI 关键交互抽测即可。
