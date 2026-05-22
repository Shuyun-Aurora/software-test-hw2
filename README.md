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
- TC02：商品排序，包含名称升序、名称降序、价格升序和价格降序

测试失败时会在 `artifacts/screenshots/` 下保存截图。
