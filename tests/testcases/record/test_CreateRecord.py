from playwright.sync_api import sync_playwright, expect
import time
import allure
import pytest

@allure.step("Test create a new record")
def test_get_example():
    with allure.step("Initialize Playwright and browser"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # Inject the script to set localStorage items before any page loads
            jwt_token = "Bearer eyJraWQiOiI3ZTAwZWRjZC1mY2Q0LTQ5M2YtYmUxYy0yZWQ1ZDI0NWQxMDUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOWUxZWZjNy02MThjLTQ0YWEtYWMwYS0wOTMyYjY0OGVhZTQiLCJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmNvc2NlbmUuY24vc3VwZXJ0b2tlbnMtc2VydmVyL2F1dGgiLCJleHAiOjE3Mzk0MjY4MDcsInVzZXJJZCI6IjI5ZTFlZmM3LTYxOGMtNDRhYS1hYzBhLTA5MzJiNjQ4ZWFlNCIsImlhdCI6MTczNjgzNDgwNiwib3JnSWQiOiJjZjc0NmUyMy0zMjEwLTRiOGYtYmRmYS1mYjc3MWQxYWM4N2MifQ.AyKI5ltZF8Rhl7GB6hdETtdzP7rEgLcmAJMjBecO6KKok_no1OwfWvtrA9EVUhoj5dbuSsd_hpAE-AqJAIhz5ZEperai63hxJzMBKk4b0_e6_Ky5Kq-CIRSwQpixHndUF18RA3o6VLdDJPgrdgWmQHksK-ef20gO6IyEqSB5EmhiB6ZEto39DXc9M76IyUExEtOthDgPHi__OGRwb5_uIOmlUAq9f4x3eP_aMRg2dry2Bm6TMvHb58Gu1Q8VNOOguEWjWuZCKGjRD0GOo0mbvFL1xpIJkUYoGdKaERhkLUY9g42T41THU0Ux-0I5wqKyYbZF_HZbjVk415BRcClc0A"
            if not jwt_token:
                raise ValueError("CN_JWT environment variable is not set")

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

if __name__ == "__main__":
    pytest.main(["-s", "your_script_name.py", "--alluredir=./allure-results"])