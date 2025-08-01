import allure
import logging
import re
import os
from playwright.sync_api import sync_playwright
# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


@allure.story("Web API jump test")
def test_example(pytestconfig):
    with sync_playwright() as playwright:
            # 启动浏览器，设置 headless 为 True 用于无头模式适应 Linux 环境
        browser = playwright.chromium.launch(headless=False)  # 无头模式
        context = browser.new_context()

        # token = pytestconfig.getini("jwt_token_lark")
        token = os.environ.get("JWT_TOKEN")
        if not token:
            raise ValueError("JWT token is not set")

        logger.info("设置 localStorage 的 JWT 和语言信息...")
        with allure.step("Set JWT in localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)

        logger.info("打开页面...")
        page = context.new_page()
        with allure.step("Navigate and execute tests"):
            navigate_to_organization(page)
            add_associated_projects(page)
            explore_projects(page)


@allure.step("Navigate through the organization")
def navigate_to_organization(page):
    logger.info("导航到组织管理页面...")
    page.goto("https://staging.coscene.cn/org/projects", wait_until="domcontentloaded", timeout=60000)
    logger.info("页面加载完成。")
    page.get_by_role("radio", name="已归档").click()
    page.get_by_role("button", name="成员").click()
    page.get_by_role("radio", name="已禁用").click()
    page.get_by_role("button", name="设备").click()
    page.get_by_role("button", name="添加设备").click()
    page.get_by_role("button", name="离线安装").click()
    page.get_by_role("button", name="手动录入").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="设备配置").click()
    page.get_by_role("button", name="取消").click()
    # page.get_by_role("button", name="网络").click()
    page.get_by_role("button", name="镜像").click()
    page.get_by_role("button", name="可视化布局配置").click()
    page.get_by_role("button", name="设置").click()
    page.get_by_text("自定义字段").click()
    page.get_by_text("设备字段配置").click()
    page.get_by_text("角色管理").click()
    page.get_by_role("button", name="用量与计费").click()
    page.get_by_role("button", name="审计").click()


@allure.step("Add associated projects to devices")
def add_associated_projects(page):
    logger.info("添加关联项目到设备...")
    try:
        page.get_by_role("button", name="设备").click()
        page.get_by_role("row", name="ID 名称 客户端状态 更新时间 创建时间 关联项目").locator("label div").nth(
            3).click()
        page.get_by_role("button", name="添加关联项目").click()
        page.get_by_role("combobox").click()
        page.get_by_role("option", name="q2").first.click()
        page.get_by_role("button", name="添加").click()
        page.get_by_role("link", name="coScene-logo").click()
        page.get_by_role("button", name="探索公开项目").click()
    except Exception as e:
        logger.warning(f"添加关联项目过程中发生错误: {e}")


@allure.step("Explore projects and interactions")
def explore_projects(page):
    logger.info("探索项目并进行交互...")
    try:
        page.get_by_role("link", name="coScene-logo").click()
        page.get_by_text("🅱️Bubbl自动化测试专属项目测试数据，勿动内部").click()
        page.get_by_role("button", name="Close").click()
        page.get_by_role("button", name="概览").click()
        page.get_by_role("button", name="仪表盘").click()
        page.get_by_role("button", name="记录").click()
        page.get_by_role("button", name="任务").click()
        page.get_by_text("通用任务").click()
        page.get_by_text("标注任务").click()
        page.get_by_role("button", name="自动化").click()
        page.wait_for_timeout(500)
        page.get_by_role("button", name="触发器").click()
        page.wait_for_timeout(500)
        page.get_by_role("button", name="调用历史").click()
        page.wait_for_timeout(500)
        page.get_by_role("button", name="批量测试").click()
        page.get_by_role("button", name="测试程序管理").click()
        page.get_by_role("button", name="批量测试").click()
        page.get_by_role("button", name="测试套件管理").click()
        page.get_by_role("button", name="设备").click()
        page.get_by_role("button", name="添加设备").click()
        page.get_by_role("button", name="命令行安装").click()
        page.get_by_role("button", name="离线安装").click()
        page.get_by_role("button", name="手动录入").click()
        page.get_by_role("button", name="Close").click()
        page.get_by_role("button", name="规则&定位").click()
        page.get_by_role("button", name="执行历史").click()
        page.get_by_role("button", name="资源").click()
        page.get_by_role("button", name="设置").click()
        page.get_by_role("button", name="添加成员").click()
        page.get_by_role("button", name="取消").click()
        page.get_by_text("服务集成").click()
        page.get_by_text("可视化布局配置").click()
        page.get_by_text("基本设置").click()
        page.get_by_text("高级设置").click()
        page.locator("div").filter(has_text=re.compile(r"^为本项目模块配置字段，在创建/编辑时填写，支持在页面自定义展示编辑配置$")).get_by_role("button").click()
        page.get_by_text("任务字段").click()
        page.get_by_text("一刻字段").click()
        page.get_by_role("button", name="添加字段").click()
        page.get_by_role("button", name="取消").click()
        page.get_by_role("button", name="设置").click()
        page.get_by_text("高级设置").click()
        page.get_by_role("button", name="编辑预留时长").click()
        page.get_by_role("button", name="取消").click()
        page.get_by_role("button", name="切换可见性").click()
        page.get_by_role("button", name="取消").click()
        page.get_by_role("button", name="归档项目").click()
        page.get_by_role("button", name="取消").click()
        page.get_by_role("button", name="删除项目").click()
        page.get_by_role("button", name="取消").click()
    except Exception as e:
        logger.warning(f"探索项目过程中发生错误: {e}")


if __name__ == "__main__":
    test_example()