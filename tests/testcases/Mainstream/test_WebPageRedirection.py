# import allure
# from playwright.sync_api import sync_playwright
#
#
# @allure.step("Test web page redirection")
# def test_example(page=None):
#     with sync_playwright() as playwright:
#         # 启动浏览器
#         browser = playwright.chromium.launch(headless=False)
#         context = browser.new_context()
#         jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
#
#         if not jwt_token:
#             raise ValueError("CN_JWT environment variable is not set")
#
#         with allure.step("Set JWT in localStorage"):
#             context.add_init_script(f"""
#                 localStorage.setItem('coScene_org_jwt', '{jwt_token}');
#                 localStorage.setItem('i18nextLng', 'cn');
#             """)
#         # 打开页面
#         page = context.new_page()
#         with allure.step("go to the organization"):
#             page.goto("https://staging.coscene.cn/org/projects")
#             page.wait_for_timeout(1000)
#             page.get_by_role("button", name="成员").click()
#             # page.wait_for_timeout(1000)
#             page.get_by_role("button", name="设备").click()
#             page.get_by_role("button", name="网络").click()
#             page.get_by_role("button", name="镜像").click()
#             page.get_by_role("button", name="可视化布局配置").click()
#             page.get_by_role("button", name="设置").click()
#             page.get_by_role("button", name="用量与计费").click()
#             page.get_by_role("button", name="审计").click()
#
#         with allure.step("go to the devices add associated projects"):
#             page.get_by_role("link", name="coScene-logo").click()
#             page.wait_for_timeout(1000)
#             page.get_by_text("前往组织管理").click()
#             page.get_by_role("button", name="设备").click()
#             page.get_by_role("row", name="ID 名称 客户端状态 更新时间 创建时间 关联项目").get_by_label("").check()
#             page.get_by_role("button", name="添加关联项目").click()
#             page.get_by_role("combobox").click()
#             page.get_by_text("q2").first.click()
#             page.wait_for_timeout(1000)
#             page.get_by_role("button", name="添加").click()
#             page.wait_for_timeout(1000)
#
#         with allure.step("go to the projects"):
#             page.get_by_role("link", name="coScene-logo").click()
#             page.wait_for_timeout(1000)
#             page.get_by_role("button", name="探索公开项目").click()
#             page.get_by_role("link", name="coScene-logo").click()
#             page.wait_for_timeout(1000)
#             page.get_by_text("Bubbl自动化测试专属项目测试数据，勿动内部").first.click()
#             page.get_by_role("button", name="仪表盘").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="任务").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("通用任务").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("标注任务").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("采集任务").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="自动化").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("动作").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("触发器").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("调用历史").click()
#             page.wait_for_timeout(1000)
#             page.get_by_role("button", name="批量测试").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="数采&诊断").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="项目设备", exact=True).click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="项目概览").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("button", name="项目设置").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("服务集成").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("可视化布局配置").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("基本设置").click()
#             page.wait_for_timeout(500)
#             page.get_by_text("高级设置").click()
#             page.wait_for_timeout(500)
#             page.get_by_role("link", name="coScene-logo").click()
#             page.wait_for_timeout(1000)
#
# if __name__ == "__main__":
#     test_example()

#-----------------------------------------------------------------------------------------------------------------------

import allure
import logging
from playwright.sync_api import sync_playwright
# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


@allure.step("Test web page redirection")
def test_example():
    with sync_playwright() as playwright:
        try:
            logger.info("启动浏览器...")
            # 启动浏览器，设置 headless 为 True 用于无头模式适应 Linux 环境
            browser = playwright.chromium.launch(headless=False)  # 无头模式
            context = browser.new_context()

            jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
            if not jwt_token:
                raise ValueError("JWT token is not set")

            logger.info("设置 localStorage 的 JWT 和语言信息...")
            with allure.step("Set JWT in localStorage"):
                context.add_init_script(f"""
                    localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                    localStorage.setItem('i18nextLng', 'cn');
                """)

            logger.info("打开页面...")
            page = context.new_page()
            with allure.step("Navigate and execute tests"):
                navigate_to_organization(page)
                add_associated_projects(page)
                explore_projects(page)

        except Exception as e:
            logger.error(f"执行过程中发生错误: {e}")
        finally:
            logger.info("浏览器关闭中...")
            browser.close()
            logger.info("浏览器已关闭。")


@allure.step("Navigate through the organization")
def navigate_to_organization(page):
    logger.info("导航到组织管理页面...")
    page.goto("https://staging.coscene.cn/org/projects", wait_until="domcontentloaded", timeout=60000)
    logger.info("页面加载完成。")

    buttons = ["成员", "设备", "网络", "镜像", "可视化布局配置", "设置", "用量与计费", "审计"]
    for button_name in buttons:
        try:
            logger.info(f"点击按钮: {button_name}...")
            page.get_by_role("button", name=button_name).click()
            logger.info(f"成功点击按钮: {button_name}")
        except Exception as e:
            logger.warning(f"未能点击按钮 '{button_name}': {e}")


@allure.step("Add associated projects to devices")
def add_associated_projects(page):
    logger.info("添加关联项目到设备...")
    try:
        page.get_by_role("link", name="coScene-logo").click()
        logger.info("点击 coScene-logo 链接成功。")

        page.get_by_text("前往组织管理").click()
        logger.info("点击 '前往组织管理' 成功。")

        page.get_by_role("button", name="设备").click()
        logger.info("点击 '设备' 按钮成功。")

        page.get_by_role("row", name="ID 名称 客户端状态 更新时间 创建时间 关联项目").get_by_label("").check()
        logger.info("选中设备行复选框成功。")

        page.get_by_role("button", name="添加关联项目").click()
        logger.info("点击 '添加关联项目' 按钮成功。")

        page.get_by_role("combobox").click()
        logger.info("点击下拉框成功。")

        page.get_by_text("q2").first.click()
        logger.info("选择项目 'q2' 成功。")

        page.get_by_role("button", name="添加").click()
        logger.info("点击 '添加' 按钮成功。")
    except Exception as e:
        logger.warning(f"添加关联项目过程中发生错误: {e}")


@allure.step("Explore projects and interactions")
def explore_projects(page):
    logger.info("探索项目并进行交互...")
    try:
        page.get_by_role("link", name="coScene-logo").click()
        logger.info("点击 coScene-logo 链接成功。")

        page.get_by_role("button", name="探索公开项目").click()
        logger.info("点击 '探索公开项目' 按钮成功。")

        page.get_by_role("link", name="coScene-logo").click()
        page.get_by_text("Bubbl自动化测试专属项目测试数据，勿动内部").first.click()
        logger.info("进入指定项目成功。")

        project_buttons = [
            "仪表盘", "任务", "自动化", "批量测试", "数采&诊断",
            "项目设备", "项目概览", "项目设置"
        ]
        for button in project_buttons:
            try:
                logger.info(f"点击项目按钮: {button}...")
                page.get_by_role("button", name=button, exact=True).click()
                logger.info(f"成功点击项目按钮: {button}")
            except Exception as e:
                logger.warning(f"未能点击项目按钮 '{button}': {e}")

        settings_texts = ["服务集成", "可视化布局配置", "基本设置", "高级设置"]
        for text_item in settings_texts:
            try:
                logger.info(f"点击设置选项: {text_item}...")
                page.get_by_text(text_item).click()
                logger.info(f"成功点击设置选项: {text_item}")
            except Exception as e:
                logger.warning(f"未能点击设置选项 '{text_item}': {e}")

        page.get_by_role("link", name="coScene-logo").click()
        logger.info("返回首页成功。")

    except Exception as e:
        logger.warning(f"探索项目过程中发生错误: {e}")


if __name__ == "__main__":
    test_example()