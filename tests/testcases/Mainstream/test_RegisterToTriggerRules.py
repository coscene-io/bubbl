import re
import logging
import allure
from playwright.sync_api import sync_playwright, Page

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


@allure.step("创建新项目")
def create_new_project(page: Page) -> None:
    logger.info("点击 '新建项目' 按钮")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="新建项目").click()
    page.wait_for_timeout(1000)

    logger.info("选择 '新建空白项目'")
    page.locator("div").filter(has_text=re.compile(r"^新建空白项目$")).nth(1).click()
    page.wait_for_timeout(1000)

    logger.info("填写项目名称为 'test5'")
    page.get_by_placeholder("输入项目名称").fill("test5")
    page.get_by_text("test5").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '完成创建' 按钮")
    page.get_by_role("button", name="完成创建").click()
    page.wait_for_timeout(1000)


@allure.step("配置规则组")
def configure_rule_group(page: Page) -> None:
    logger.info("点击 '数采&诊断' 按钮")
    page.get_by_role("button", name="数采&诊断").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '添加规则组' 按钮")
    page.get_by_role("button", name="添加规则组").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '创建' 按钮")
    page.get_by_role("button", name="创建").click()
    page.wait_for_timeout(1000)

    logger.info("选择 '未命名规则组(0)'")
    page.get_by_text("未命名规则组(0)").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '创建空白规则'")
    page.get_by_role("button", name="创建空白规则").click()
    page.wait_for_timeout(1000)

    logger.info("填写规则名称为 'bag'")
    page.get_by_placeholder("未命名规则").fill("bag")
    page.wait_for_timeout(1000)


@allure.step("设置规则详情")
def set_rule_details(page: Page) -> None:
    logger.info("点击 '自动化' 按钮")
    page.get_by_role("button", name="自动化").click()
    page.wait_for_timeout(1000)

    logger.info("选择话题")
    page.locator("button").filter(has_text="选择话题").click()
    page.get_by_text("/version").click()
    page.wait_for_timeout(1000)

    logger.info("填写设备消息字段 'msg.version'")
    page.get_by_placeholder("设备消息字段，如 msg.message").click()
    page.get_by_placeholder("设备消息字段，如 msg.message").fill("msg.version")
    page.wait_for_timeout(1000)

    logger.info("设置事件匹配条件")
    page.locator("div").filter(
        has_text=re.compile(r"^事件匹配条件切换为代码模式包含事件码表 code 列任一行的值并且$")).get_by_role(
        "button").nth(2).click()
    page.get_by_placeholder("请输入具体值").fill("1.0.6-5-g385eb3f")
    page.wait_for_timeout(1000)

    logger.info("点击 '更多设置'")
    page.locator("div").filter(has_text=re.compile(r"^更多设置$")).get_by_role("img").click()
    page.locator("div:nth-child(2) > .text-gray-900 > .space-y-2 > .-mx-1 > .w-0 > .flex").click()
    page.get_by_placeholder("输入文件在设备中的地址，如：/home/map.png").fill(
        "/home/just2004noetic/Downloads/dev-A.log")
    page.wait_for_timeout(1000)

    logger.info("选择诊断数据和确认选项")
    page.get_by_label("诊断数据").check()
    page.get_by_label("是").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '创建' 按钮")
    page.get_by_role("button", name="创建", exact=True).click()
    page.wait_for_timeout(1000)


@allure.step("管理设备")
def manage_devices(page: Page) -> None:
    logger.info("返回到组织管理")
    page.get_by_role("link", name="coScene-logo").click()
    page.get_by_text("前往组织管理").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '设备' 按钮")
    page.get_by_role("button", name="设备").click()
    page.wait_for_timeout(1000)

    logger.info("点击 '添加设备' 按钮")
    page.get_by_role("button", name="添加设备").click()
    page.wait_for_timeout(1000)

    logger.info("选择系统生成 ID")
    page.get_by_label("系统生成 ID").click()
    page.wait_for_timeout(1000)

    logger.info("完成设备添加流程")
    page.get_by_label("添加设备").locator(
        "div").filter(has_text="在设备端执行命令添加使用离线安装包添加填写信息添加设备系统").locator("button").nth(3).click()
    page.get_by_role("dialog").nth(1).click()
    page.get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)


@allure.title("完整测试用例")
def test_example() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
        if not jwt_token:
            raise ValueError("JWT token is missing!")

        with allure.step("设置 JWT 到 localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)

        page = context.new_page()
        logger.info("开始执行测试用例")
        create_new_project(page)
        configure_rule_group(page)
        set_rule_details(page)
        manage_devices(page)
        logger.info("测试用例执行完成")