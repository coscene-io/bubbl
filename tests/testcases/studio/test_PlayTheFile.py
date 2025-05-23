from playwright.sync_api import sync_playwright, expect
import time
import allure

@allure.story("Visual file playback")
def test_get_example():
    with allure.step("Initialize Playwright and browser"):
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # JWT token for authentication
            jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
            if not jwt_token:
                raise ValueError("CN_JWT environment variable is not set")

            # Inject the script to set localStorage items before any page loads
            with allure.step("Set JWT in localStorage"):
                context.add_init_script(f"""
                    localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                    localStorage.setItem('i18nextLng', 'cn');
                """)

            page = context.new_page()

            with allure.step("Navigate to the records page"):
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records", timeout=3 * 60 * 1000)

            with allure.step("Perform actions on the records page"):
                with allure.step("Click on the specific record link"):
                    page.get_by_role("link", name="播放文件").click()
                with allure.step("Click on the '播放记录' button and handle popup"):
                    with page.expect_popup() as page_info:
                        page.get_by_role("button", name="播放记录").click()
                    page = page_info.value

                with allure.step("Interact with the popup page"):
                    page.wait_for_timeout(5000)
                    page.get_by_label("播放").click()
                    page.goto("https://staging.coscene.cn/viz?ds=coscene-data-platform&ds.key=TTjPYEk3pFmz0ENw7uKI3&layoutId=76ecfb33-806a-41d9-8ced-d097874bbd3b&time=2023-08-31T09%3A46%3A12.661000000Z")
                    page.wait_for_timeout(5000)
                    page.get_by_label("播放").click()
                    page.wait_for_timeout(5000)

            with allure.step("Close the browser"):
                browser.close()

#if __name__ == "__main__":
#    pytest.main(["-s", "your_script_name.py", "--alluredir=./allure-results"])