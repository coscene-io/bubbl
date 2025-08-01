import logging
from playwright.sync_api import sync_playwright, expect
import allure
import os

# 配置logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

@allure.story("Test create a new record")
def test_get_example(page=None):
    with allure.step("Initialize Playwright and browser"):
        logging.info("Initializing Playwright and browser...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            token = os.environ.get("JWT_TOKEN")
            if not token:
                raise ValueError("CN_JWT environment variable is not set")

            with allure.step("Set JWT in localStorage"):
                logging.info("Setting JWT and language in localStorage...")
                context.add_init_script(f"""
                    localStorage.setItem('coScene_org_jwt', '{token}');
                    localStorage.setItem('i18nextLng', 'cn');
                """)
            page = context.new_page()
            logging.info("New page created.")

            with allure.step("Navigate to the records page"):
                logging.info("Navigating to https://staging.coscene.cn/coscene-lark/bubbl/records ...")
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records")

            with allure.step("Reload the records page with JWT"):
                logging.info("Reloading the records page with JWT...")
                page.goto("https://staging.coscene.cn/coscene-lark/bubbl/records", timeout=1000)
            logging.info("Attempting to close welcome dialog...")
            page.get_by_role("button", name="Close").click()
            logging.info("Closed welcome video.")
            page.get_by_role("button", name="创建记录").click()
            page.wait_for_timeout(500)
            logging.info("'创建记录' button clicked.")
            page.get_by_role("button", name="创建").click()
            page.wait_for_timeout(500)
            logging.info("'创建' button clicked.")
            page.get_by_role("button", name="记录", exact=True).click()
            logging.info("'记录' button clicked.")
            page.wait_for_timeout(1000)

            with allure.step("Close the browser"):
                browser.close()
                logging.info("Browser closed.")
