import re
import allure
from playwright.sync_api import sync_playwright, Page, expect

@allure.feature("Create project testing")
def test_example_with_token():
    with sync_playwright() as playwright:
        # 启动浏览器
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        jwt_token = "Basic YXBpa2V5Ok16UXlPR1JoT1dFMFlqVTNZMk14TjJZME9XSmhaREkzWldNM05EVmtaRGt3WXpSa1pqVTFaV0ZpT1RsaE5tVmtZVFptTkRVeU9XRXdNREZrTkRJMFlRPT0="
        if not jwt_token:
            raise ValueError("CN_JWT environment variable is not set")

        with allure.step("Set JWT in localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
        # 打开页面
        page = context.new_page()
        with allure.step("打开项目页面"):
            page.goto("https://staging.coscene.cn/")
            page.get_by_text("自动上传内部").click()
            page.wait_for_timeout(2000)



if __name__ == "__main__":
    test_example_with_token()