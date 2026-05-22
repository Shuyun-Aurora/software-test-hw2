# Appium 移动端 Web UI 测试环境搭建参考（AI生成，仅供参考）

> 适用场景：在 Windows 电脑上，使用 Appium + Android 模拟器 + Chrome 浏览器，对 SauceDemo 进行移动端 Web UI 轻量抽测。  
> 本部分是桌面端 Selenium 测试的补充，不替代 TC01--TC07 的主要 Web 自动化测试。

## 1. 测试定位

移动端测试只做关键交互抽测，不重复执行完整购物流程。建议覆盖：

1. Android Chrome 打开 SauceDemo 登录页；
2. 输入账号密码并登录；
3. 检查商品列表页关键元素可见；
4. 滑动商品列表页面；
5. 点击一个 Add to cart 按钮；
6. 检查购物车数量标记更新。

如果 Appium 环境搭建失败，可回退为 Chrome mobile emulation 或 Selenium 设置移动端窗口尺寸。回退方案只能说明页面在移动端视口下的显示和基础交互情况，不等同于完整移动端设备测试。

## 2. 测试链路

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

也就是说，Python 脚本通过 Appium Server 操作 Android 模拟器中的 Chrome 浏览器。

## 3. 需要安装的软件

需要提前准备：

1. Android Studio；
2. Android SDK Platform-Tools；
3. Android Emulator；
4. Android 模拟器，例如 Pixel 5 / Pixel 6；
5. Node.js LTS；
6. Appium；
7. Appium UiAutomator2 Driver；
8. 项目已有 conda 环境 `saucedemo-gui-test`；
9. Python 依赖 `pytest`、`selenium`、`Appium-Python-Client`。

不建议在 Windows 上选择 iOS 测试，因为 iOS 自动化通常依赖 macOS 和 Xcode。

## 4. 安装 Android Studio 与模拟器

先从 Android Studio 官网下载安装包：

```text
https://developer.android.com/studio
```

Windows 下下载 `.exe` 安装程序后双击安装，安装选项保持默认即可。首次启动 Android Studio 时选择 `Standard` 配置，接受 SDK License，并等待 Android SDK、Platform-Tools、Emulator 等组件下载完成。

安装完成后，进入：

```text
File / Settings
→ Languages & Frameworks
→ Android SDK
```

确认安装：

```text
Android SDK Platform-Tools
Android SDK Build-Tools
Android Emulator
Android SDK Platform，例如 Android 13 或 Android 14
```

然后在 Android Studio 中打开：

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

选择 Google APIs 或 Google Play 镜像，是为了保证模拟器中有 Chrome 浏览器。创建完成后启动模拟器，并确认模拟器内可以打开 Chrome。

## 5. 配置 adb

Android SDK 默认路径通常是：

```text
C:\Users\你的用户名\AppData\Local\Android\Sdk
```

在 Windows 环境变量中配置：

```text
ANDROID_HOME=C:\Users\你的用户名\AppData\Local\Android\Sdk
```

并在 `Path` 中加入：

```text
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\emulator
```

重新打开 PowerShell，执行：

```powershell
adb version
adb devices
```

如果模拟器已经启动，`adb devices` 应看到类似结果：

```text
List of devices attached
emulator-5554    device
```

如果看不到 `device`，需要先解决模拟器或 adb 配置问题，否则 Appium 测试无法继续。

## 6. 安装 Appium

安装 Node.js后（按理来说我们都安装过），重新打开 PowerShell，确认：

```powershell
node -v
npm -v
```

安装 Appium：

```powershell
npm install -g appium
appium -v
```

安装 Android 自动化驱动：

```powershell
appium driver install uiautomator2
appium driver list --installed
```

确认已安装列表中包含 `uiautomator2`。

## 7. 准备 Python 依赖

本项目使用已有 conda 环境即可。

在项目根目录执行：

```powershell
conda activate saucedemo-gui-test
pip install Appium-Python-Client
```

如果后续需要把移动端依赖固化到项目中，可以再补充到 `environment.yml` 或依赖说明中。

## 8. 启动 Appium Server

新开一个 PowerShell 窗口，执行：

```powershell
appium
```

看到 4723 端口监听信息即可，例如：

```text
Appium REST http interface listener started on http://0.0.0.0:4723
```

这个窗口需要保持打开，测试脚本会连接：

```text
http://127.0.0.1:4723
```

## 9. 最小冒烟测试

在编写正式 TC08 前，建议先确认 Appium 能打开 Android Chrome 并访问 SauceDemo。

可新建：

```text
tests/test_appium_smoke.py
```

参考内容：

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_open_saucedemo_in_android_chrome():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.device_name = "Android Emulator"

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        driver.get("https://www.saucedemo.com/")
        assert "Swag Labs" in driver.title
    finally:
        driver.quit()
```

运行：

```powershell
python -m pytest tests/test_appium_smoke.py -v
```

该测试通过后，再继续编写 TC08。

## 10. TC08 建议检查点

TC08 不需要覆盖完整结算流程，建议只检查：

1. 登录页能够在 Android Chrome 中打开；
2. 用户名、密码输入框可以输入；
3. Login 按钮可以触控点击；
4. 登录后进入商品列表页；
5. 商品列表可以滑动浏览；
6. 点击 Add to cart 后购物车数量标记变为 1；
7. 点击购物车入口后可以进入购物车页面。

如果使用 `driver.swipe()` 不稳定，可以临时改为：

```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

报告中可说明：移动端滑动操作在 Appium 环境下存在兼容性差异，测试中使用 JavaScript 滚动作为补充验证方式。

## 11. 常见问题

### 11.1 `adb devices` 看不到模拟器

优先检查：

1. Android 模拟器是否已经启动；
2. `ANDROID_HOME` 是否配置正确；
3. `Path` 是否包含 `%ANDROID_HOME%\platform-tools`；
4. PowerShell 是否在配置环境变量后重新打开。

### 11.2 `appium driver list --installed` 没有 `uiautomator2`

执行：

```powershell
appium driver install uiautomator2
appium driver list --installed
```

### 11.3 pytest 连接不上 `127.0.0.1:4723`

通常是 Appium Server 没有启动，或启动 Appium 的 PowerShell 窗口被关闭。重新执行：

```powershell
appium
```

### 11.4 模拟器中没有 Chrome

重新创建模拟器，选择 Google APIs 或 Google Play 镜像。

### 11.5 ChromeDriver 版本不兼容

如果出现 `session not created`、`chromedriver version mismatch`、`cannot automate Chrome` 等错误，可以尝试：

1. 更新 Appium 和 UiAutomator2 Driver；
2. 更换 Android 模拟器系统版本；
3. 降级或更新模拟器中的 Chrome；
4. 若仍无法解决，使用 Chrome mobile emulation 作为回退方案，并在报告中说明。

## 12. 推荐执行顺序

实际操作时按下面顺序验证：

```text
1. 启动 Android 模拟器
2. 执行 adb devices，确认看到 emulator-5554 device
3. 执行 appium driver list --installed，确认存在 uiautomator2
4. 新开 PowerShell 执行 appium，保持 Appium Server 运行
5. 激活 conda 环境 saucedemo-gui-test
6. 执行 test_appium_smoke.py
7. 冒烟测试通过后，再执行 TC08 移动端 Web UI 轻量抽测
```

## 13. 最低成功标准

满足以下三点即可认为移动端 Web UI 测试环境基本可用：

1. `adb devices` 能看到 Android 模拟器；
2. Appium Server 能在 4723 端口正常启动；
3. 冒烟测试能打开 Android Chrome 并访问 SauceDemo。

如果 TC08 也能通过，则可以在测试报告中补充移动端 Web UI 关键交互抽测结果；如果 Appium 环境未能搭建成功，则执行回退方案并说明原因。
