from playwright.sync_api import sync_playwright, expect
import time
import allure
import pytest

@allure.step("Test create a new record")
def test_get_example(page=None):
    with allure.step("Initialize Playwright and browser"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            # Inject the script to set localStorage items before any page loads
            # jwt_token = "Bearer eyJraWQiOiI3ZTAwZWRjZC1mY2Q0LTQ5M2YtYmUxYy0yZWQ1ZDI0NWQxMDUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOWUxZWZjNy02MThjLTQ0YWEtYWMwYS0wOTMyYjY0OGVhZTQiLCJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmNvc2NlbmUuY24vc3VwZXJ0b2tlbnMtc2VydmVyL2F1dGgiLCJleHAiOjE3NDcyMTA1NzMsInVzZXJJZCI6IjI5ZTFlZmM3LTYxOGMtNDRhYS1hYzBhLTA5MzJiNjQ4ZWFlNCIsImlhdCI6MTc0NDYxODU3Miwib3JnSWQiOiJjZjc0NmUyMy0zMjEwLTRiOGYtYmRmYS1mYjc3MWQxYWM4N2MifQ.ODgK8iLWawnMhatI3hcqd69qrox_gF0QlbnQbLQd4-mOEz2ttk90mCN_AsSNulr31b99GGnt7FIQ4qLqoN-T4BvleCEWTAYdN7h8PGokVefAOxG7AJucfQAZ5V2VvEiLEYbuMdVb6GRmOw980vHkAm7Dd9X6eLkyiPo1ZWbqLjyH-eQXC65zxR5PhI6VwkZcNrbuMSevjsscNY6Hhq5Wjy_ISz_qI3MFoLkWUKFpqONG4e3r5SfxjoRuOJ-IARBunhbzQLUSQCodcak_v4F97KnpetZy120rey9HCr6LWPgqpNQyl0Sy-CB5u6gun0eteVuVHDecQkBZuDsMEQ_0Jg"
            jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
            if not jwt_token:
                raise ValueError("CN_JWT environment variable is not set")

            with allure.step("Set JWT in localStorage"):
                context.add_init_script(f"""
                    localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                    localStorage.setItem('i18nextLng', 'cn');
                """)

            page = context.new_page()

            with allure.step("Navigate to the records page"):
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records")

            with allure.step("Reload the records page with JWT"):
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records", timeout=1000)

            with allure.step("Click on '创建记录' button"):
                page.get_by_role("button", name="创建记录").nth(2).click()

            with allure.step("Fill in the record name"):
                page.get_by_placeholder("输入记录名称").click()
                record_name = time.strftime("新记录" + "%Y-%m-%d_%H_%M_%S")
                page.get_by_placeholder("输入记录名称").fill(record_name)
                page.wait_for_timeout(1000)

            with allure.step("Click on '创建' button"):
                page.get_by_role("button", name="创建").click()
                page.reload()
                page.wait_for_timeout(1500)
                with allure.step("Verify the record was created successfully"):
                    # Assert the new record is present in the list
                    expect(page.locator(f"text={record_name}")).to_be_visible()

            with allure.step("Close the browser"):
                browser.close()

#if __name__ == "__main__":
#    pytest.main(["-s", "your_script_name.py", "--alluredir=./allure-results"])