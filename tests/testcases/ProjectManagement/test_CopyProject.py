import re
import os
import allure
from playwright.sync_api import sync_playwright, Page, expect
import datetime
@allure.feature("Create project testing")
def test_example_with_token():
    with sync_playwright() as playwright:
        now_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        project_slug = f"cjfzxm{now_str}"
        project_name = f"pytest创建复制项目{now_str}"
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

        with allure.step("点击新建项目"):
            page.get_by_role("button", name="新建项目").click()
            page.wait_for_timeout(1000)

        with allure.step("复制已有项目"):
            page.locator("div").filter(has_text=re.compile(r"^从已有项目复制$")).first.click()
            page.wait_for_timeout(1000)

        with allure.step("输入项目slug"):
            page.get_by_placeholder("输入项目网址（slug）").fill(project_slug)
            page.locator("div:nth-child(2) > .text-gray-900 > .flex").first.click()
            page.wait_for_timeout(1000)

        with allure.step("输入新项目名称"):
            page.get_by_placeholder("输入项目名称").fill(project_name)
            page.wait_for_timeout(1000)

        with allure.step("选择复制的项目"):
            page.get_by_role("combobox").click()
            page.wait_for_timeout(500)
            page.get_by_role("option", name="规则简化专用项目").click()
            page.wait_for_timeout(500)

        with allure.step("完成创建"):
            page.get_by_role("button", name="完成创建").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Close").click()
            page.wait_for_timeout(1000)

if __name__ == "__main__":
    test_example_with_token()