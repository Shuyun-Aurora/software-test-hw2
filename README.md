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

运行成员 B 负责的 TC03、TC04 和 TC05：

```powershell
conda activate saucedemo-gui-test
python -m pytest tests/test_tc03_product_detail.py tests/test_tc04_add_to_cart.py tests/test_tc05_cart_page.py
```

运行当前全部测试：

```powershell
conda activate saucedemo-gui-test
python -m pytest
```

当前包含：

- TC01：登录后进入商品浏览流程
- TC02：商品排序，包含名称升序、名称降序、价格升序和价格降序
- TC03：查看商品详情，检查商品名称、描述、价格、图片和返回入口
- TC04：添加商品到购物车，检查按钮状态和购物车 badge 数量变化
- TC05：购物车页面检查，检查商品名称、描述、价格、数量和结算入口

测试失败时会在 `artifacts/screenshots/` 下保存截图。
