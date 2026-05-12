# SauceDemo GUI 自动化测试

本项目使用 `Python + Selenium + pytest` 对 SauceDemo 电商网站进行 GUI 自动化测试。

## 环境与依赖

建议使用单独的 conda 环境：

```powershell
conda create -n saucedemo-gui-test python=3.11 -y
conda activate saucedemo-gui-test
python -m pip install -r requirements.txt
```

也可以通过 `environment.yml` 创建：

```powershell
conda env create -f environment.yml
```

## 运行测试

运行成员 A 负责的 TC01 和 TC02：

```powershell
conda activate saucedemo-gui-test
python -m pytest tests/test_tc01_login_inventory.py tests/test_tc02_product_sorting.py
```

当前包含：

- TC01：登录后进入商品浏览流程
- TC02：商品排序，包含名称降序和价格升序

测试失败时会在 `artifacts/screenshots/` 下保存截图。

## 说明

正常本机运行推荐使用有界面模式，便于观察浏览器操作过程。无界面模式可选：

```powershell
python -m pytest tests/test_tc01_login_inventory.py tests/test_tc02_product_sorting.py --headless
```

开发过程中曾在沙箱环境下遇到无界面 Chrome DevTools 断连问题，加入稳定参数后已可运行。该问题更可能与沙箱/CI 环境有关，本机有界面模式通过即可认为当前用例可执行。
