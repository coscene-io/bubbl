import allure
import logging
import re
from playwright.sync_api import sync_playwright

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

OPS_URL = "https://ops.staging.coscene.cn/organizations"
STAGING_URL = "https://staging.coscene.cn/org/projects"

@allure.story("Web API jump test")
def test_example(pytestconfig):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)  # 性能更优，建议无头
        context = browser.new_context()

        token = pytestconfig.getini("jwt_token_lark_46email")
        if not token:
            raise ValueError("JWT token is not set")

        context.add_init_script(f"""
            localStorage.setItem('coScene_org_jwt', '{token}');
            localStorage.setItem('i18nextLng', 'cn');
        """)

        page = context.new_page()
        try:
            Enable_usage_limit(page)
            navigate_to_organization(page)
            Turn_off_usage_restrictions(page)
        except Exception as e:
            logger.error(f"测试过程发生错误: {e}")
        finally:
            page.close()
            browser.close()

@allure.step("Enable usage limit (OPS)")
def Enable_usage_limit(page):
    page.goto(OPS_URL, wait_until="domcontentloaded", timeout=30000)
    page.get_by_role("button", name="客户管理").click()
    page.get_by_role("button", name="2").click()
    page.get_by_role("link", name="46邮箱组织2").click()
    page.locator("div").filter(has_text=re.compile(r"^存储空间（GB）套餐10\.00已使用16\.24使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^公开项目存储空间（GB）套餐500\.00已使用2\.37使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^流出流量（GB）套餐10\.00已使用0\.00使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^计算时长（分钟）套餐500\.00已使用0\.00使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^活跃设备数（台）套餐1已使用1使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^用户席位（人）套餐3已使用3使用限制已关闭$")).get_by_role("switch").click()
    page.wait_for_timeout(500)

@allure.step("Navigate organization (STAGING)")
def navigate_to_organization(page):
    page.goto(STAGING_URL, wait_until="domcontentloaded", timeout=30000)
    page.get_by_role("radio", name="已归档").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="成员").click()
    page.wait_for_timeout(1000)
    page.get_by_role("radio", name="已禁用").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="设置").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="用量与计费").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="coScene-logo").click()
    page.get_by_text("回归测试项目重要项目，勿删勿动！内部").first.click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="概览").click()
    page.get_by_role("button", name="S3 连接").click()
    page.get_by_role("button", name="设置").click()
    page.get_by_role("button", name="添加成员").click()
    page.get_by_role("button", name="取消").click()
    page.get_by_text("基本设置").click()
    page.get_by_text("高级设置").click()
    page.get_by_role("button", name="切换可见性").click()
    page.get_by_label("私有").click()
    page.get_by_label("公开").click()
    page.get_by_role("button", name="取消").click()
    page.get_by_role("button", name="归档项目").click()
    page.get_by_role("button", name="取消").click()
    page.get_by_role("button", name="删除项目").click()
    page.get_by_role("button", name="取消").click()


@allure.step("Turn off usage restrictions (OPS)")
def Turn_off_usage_restrictions(page):
    page.goto(OPS_URL, wait_until="domcontentloaded", timeout=30000)
    page.get_by_role("button", name="客户管理").click()
    page.get_by_role("button", name="2").click()
    page.get_by_role("link", name="46邮箱组织2").click()
    page.wait_for_timeout(1000)
    page.locator("div").filter(has_text=re.compile(r"^存储空间（GB）套餐10\.00已使用16\.24使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^公开项目存储空间（GB）套餐500\.00已使用2\.37使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^流出流量（GB）套餐10\.00已使用0\.00使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^计算时长（分钟）套餐500\.00已使用0\.00使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^活跃设备数（台）套餐1已使用1使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text=re.compile(r"^用户席位（人）套餐3已使用3使用限制已开启$")).get_by_role("switch").click()
    page.wait_for_timeout(500)


if __name__ == "__main__":
    test_example()