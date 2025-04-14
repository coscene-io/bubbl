from playwright.sync_api import sync_playwright, expect
import time
import allure

@allure.step("Test create a new record")
def test_get_example():
    with allure.step("Initialize Playwright and browser"):
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # JWT token for authentication
            # jwt_token = "Bearer eyJraWQiOiI3ZTAwZWRjZC1mY2Q0LTQ5M2YtYmUxYy0yZWQ1ZDI0NWQxMDUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOWUxZWZjNy02MThjLTQ0YWEtYWMwYS0wOTMyYjY0OGVhZTQiLCJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmNvc2NlbmUuY24vc3VwZXJ0b2tlbnMtc2VydmVyL2F1dGgiLCJleHAiOjE3NDcyMTA1NzMsInVzZXJJZCI6IjI5ZTFlZmM3LTYxOGMtNDRhYS1hYzBhLTA5MzJiNjQ4ZWFlNCIsImlhdCI6MTc0NDYxODU3Miwib3JnSWQiOiJjZjc0NmUyMy0zMjEwLTRiOGYtYmRmYS1mYjc3MWQxYWM4N2MifQ.ODgK8iLWawnMhatI3hcqd69qrox_gF0QlbnQbLQd4-mOEz2ttk90mCN_AsSNulr31b99GGnt7FIQ4qLqoN-T4BvleCEWTAYdN7h8PGokVefAOxG7AJucfQAZ5V2VvEiLEYbuMdVb6GRmOw980vHkAm7Dd9X6eLkyiPo1ZWbqLjyH-eQXC65zxR5PhI6VwkZcNrbuMSevjsscNY6Hhq5Wjy_ISz_qI3MFoLkWUKFpqONG4e3r5SfxjoRuOJ-IARBunhbzQLUSQCodcak_v4F97KnpetZy120rey9HCr6LWPgqpNQyl0Sy-CB5u6gun0eteVuVHDecQkBZuDsMEQ_0Jg"
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
                    page.get_by_role("link", name="新记录2025-04-14_16_29_51").click()
                """with allure.step("Click on the upload button"):
                    page.get_by_role("button", name="上传").click()
                with allure.step("Select '复制文件自' from the menu"):
                    page.get_by_role("menuitem", name="复制文件自").click()
                with allure.step("Click on the combobox"):
                    page.get_by_role("combobox").click()
                with allure.step("Select 'copy_file' from the dropdown"):
                    page.get_by_text("copy_file").click()
                with allure.step("Check the file checkbox"):
                    page.get_by_role("row", name="short.bag 135.13 MB").get_by_label("").check()
                with allure.step("Click on the confirm button"):
                    page.get_by_role("button", name="确定").click()
                    page.wait_for_timeout(3000)"""
                with allure.step("Click on the '播放记录' button and handle popup"):
                    with page.expect_popup() as page_info:
                        page.get_by_role("button", name="播放记录").click()
                    page = page_info.value

                with allure.step("Interact with the popup page"):
                    page.wait_for_timeout(5000)
                    page.get_by_label("播放").click()
                    page.goto(
                        "https://staging.coscene.cn/viz?ds=coscene-data-platform&ds.key=H4z8IY3OdQkL7CKmElpbT&time=2023-08-31T09%3A46%3A19.203035434Z")
                    page.wait_for_timeout(5000)
                    page.get_by_label("播放").click()
                    page.wait_for_timeout(5000)

            with allure.step("Close the browser"):
                browser.close()

#if __name__ == "__main__":
#    pytest.main(["-s", "your_script_name.py", "--alluredir=./allure-results"])