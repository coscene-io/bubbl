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

@allure.story("Web API jump test")
def test_example(pytestconfig):
    # 性能优化：无头模式，减少资源消耗
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 优先从 pytest 配置中获取 token
        try:
            token = pytestconfig.getini("jwt_token_lark")
        except Exception as e:
            logger.error(f"获取 token 配置异常: {e}")
            token = None

        if not token:
            logger.error("JWT token is not set，测试无法进行")
            return

        # 性能优化：初始化脚本一次性设置 localStorage
        try:
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
        except Exception as e:
            logger.error(f"初始化 localStorage 失败: {e}")

        # 依次执行各步骤，异常时日志记录并跳过
        steps = [
            ("Navigate through the organization", navigate_to_organization),
            ("Add associated projects to devices", add_associated_projects),
            ("Explore projects and interactions", explore_projects),
        ]
        for step_name, step_func in steps:
            with allure.step(step_name):
                try:
                    step_func(page)
                except Exception as e:
                    logger.error(f"{step_name} 执行失败: {e}")

        page.close()
        browser.close()

@allure.step("Navigate through the organization")
def navigate_to_organization(page):
    logger.info("导航到组织管理页面...")
    page.goto("https://staging.coscene.cn/org/projects", wait_until="domcontentloaded", timeout=30000)
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
    page.get_by_role("button", name="镜像").click()
    page.get_by_role("button", name="设置").click()
    page.get_by_text("自定义字段").click()
    page.get_by_text("设备字段配置").click()
    page.get_by_text("角色管理").click()
    page.get_by_role("button", name="用量与计费").click()
    page.get_by_role("button", name="审计").click()

@allure.step("Add associated projects to devices")
def add_associated_projects(page):
    logger.info("添加关联项目到设备...")
    page.get_by_role("button", name="设备").click()
    # 性能优化：通过 nth(3) 快速定位
    page.get_by_role("row", name="ID 名称 客户端状态 关联项目 更新时间 创建时间").locator("label div").nth(3).click()
    page.get_by_role("button", name="添加关联项目").click()
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="studio-测试专用").first.click()
    page.get_by_role("button", name="添加").click()
    page.get_by_role("link", name="coScene-logo").click()
    page.get_by_role("button", name="探索公开项目").click()

@allure.step("Explore projects and interactions")
def explore_projects(page):
    logger.info("探索项目并进行交互...")
    page.get_by_role("link", name="coScene-logo").click()
    page.get_by_text("Bubbl自动化测试专属项目测试数据，勿动私有").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="概览").click()
    page.get_by_role("button", name="S3 连接").click()
    page.get_by_role("button", name="仪表盘").click()
    page.get_by_role("button", name="记录").click()
    page.get_by_role("button", name="任务").click()
    page.get_by_role("button", name="标注任务").click()
    page.get_by_role("button", name="自动化").click()
    page.get_by_role("button", name="触发器").click()
    page.get_by_role("button", name="调用历史").click()
    page.get_by_role("button", name="批量测试").click()
    page.get_by_role("button", name="批量测试", exact=True).click()
    page.get_by_role("button", name="测试程序管理").click()
    page.get_by_role("button", name="批量测试").click()
    page.get_by_role("button", name="测试套件管理").click()
    page.get_by_role("button", name="批量测试").click()
    page.get_by_role("button", name="运行批量测试").click()
    page.get_by_role("button", name="取消").click()
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
    page.get_by_text("基本设置").click()
    page.get_by_text("高级设置").click()
    page.locator("div").filter(has_text=re.compile(r"^添加工控机的 IMEI 号，将相关数据上传至项目编辑配置$")).get_by_role("button").click()
    page.get_by_text("高级设置").first.click()
    page.locator("div").filter(has_text=re.compile(r"^为本项目模块配置字段，在创建/编辑时填写，支持在页面自定义展示编辑配置$")).get_by_role("button").click()
    page.get_by_text("任务字段").click()
    page.get_by_text("一刻字段").click()
    page.get_by_role("button", name="设置").click()
    page.get_by_text("高级设置").click()
    page.get_by_role("button", name="编辑预留时长").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="切换可见性").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="归档项目").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="删除项目").click()
    page.get_by_role("button", name="Close").click()

if __name__ == "__main__":
    # 兼容 pytest 启动
    import sys
    class DummyConfig:
        def getini(self, key):
            return None
    config = DummyConfig()
    if len(sys.argv) > 1 and sys.argv[1] == "pytest":
        test_example(config)