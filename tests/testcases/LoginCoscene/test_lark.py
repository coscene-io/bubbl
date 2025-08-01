import re
import os
import allure
from playwright.sync_api import sync_playwright, Page, expect

@allure.feature("Create project testing")
def test_example_with_token():
    with sync_playwright() as playwright:
        # 启动浏览器
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        token = os.environ.get("JWT_TOKEN")
        if not token:
            raise ValueError("CN_JWT environment variable is not set")

        with allure.step("Set JWT in localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
        # 打开页面
        page = context.new_page()
        with allure.step("打开项目页面"):
            page.goto("https://staging.coscene.cn/")
            page.get_by_text("🅱️Bubbl自动化测试专属项目测试数据，勿动内部").click()
            # page.wait_for_timeout(2000)



if __name__ == "__main__":
    test_example_with_token()