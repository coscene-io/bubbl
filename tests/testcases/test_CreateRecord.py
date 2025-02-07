import os
from playwright.sync_api import sync_playwright, expect
import time
import allure

@allure.step("Test create a new record")
def test_get_example():
    with allure.step("Initialize Playwright and browser"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # 从环境变量获取 JWT token
            jwt_token = os.getenv('COSCENE_JWT_TOKEN')
            if not jwt_token:
                raise ValueError("COSCENE_JWT_TOKEN environment variable is not set")

            with allure.step("Set JWT in localStorage"):
                context.add_init_script(f"""
                    localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                    localStorage.setItem('i18nextLng', 'en');
                """)

            page = context.new_page()

            with allure.step("Navigate to the records page"):
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records")

            with allure.step("Reload the records page with JWT"):
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records", timeout=3 * 60 * 1000)

            with allure.step("Click on '创建记录' button"):
                page.get_by_role("button", name="创建记录").nth(2).click()

            with allure.step("Fill in the record name"):
                page.get_by_placeholder("输入记录名称").click()
                record_name = time.strftime("新记录" + "%Y-%m-%d_%H_%M_%S")
                page.get_by_placeholder("输入记录名称").fill(record_name)
                page.wait_for_timeout(2000)

            with allure.step("Click on '创建' button"):
                page.get_by_role("button", name="创建").click()
                page.reload()
                page.wait_for_timeout(3000)
                with allure.step("Verify the record was created successfully"):
                    # Assert the new record is present in the list
                    expect(page.locator(f"text={record_name}")).to_be_visible()

            with allure.step("Close the browser"):
                browser.close()

#if __name__ == "__main__":
#    pytest.main(["-s", "your_script_name.py", "--alluredir=./allure-results"])