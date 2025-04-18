import time
from typing import re

import allure
from playwright.sync_api import sync_playwright

@allure.step("Test web page redirection")
def test_example(page=None):
    with sync_playwright() as playwright:
        # 启动浏览器
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="

        if not jwt_token:
            raise ValueError("CN_JWT environment variable is not set")

        with allure.step("Set JWT in localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
        # 打开页面
        page = context.new_page()
        with allure.step("go to the organization"):
            page.goto("https://staging.coscene.cn/org/projects")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="成员").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="设备").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="网络").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="镜像").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="可视化布局配置").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="设置").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="用量与计费").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="审计").click()
            page.wait_for_timeout(1000)

        with allure.step("go to the devices add associated projects"):
            page.get_by_role("link", name="coScene-logo").click()
            page.wait_for_timeout(1000)
            page.get_by_text("前往组织管理").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="设备").click()
            page.wait_for_timeout(1000)
            page.get_by_role("row", name="ID 名称 客户端状态 更新时间 创建时间 关联项目").get_by_label("").check()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="添加关联项目").click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox").click()
            page.wait_for_timeout(1000)
            page.get_by_text("q2").first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="添加").click()
            page.wait_for_timeout(1000)

        with allure.step("go to the projects"):
            page.get_by_role("link", name="coScene-logo").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="探索公开项目").click()
            page.wait_for_timeout(1000)
            page.get_by_role("link", name="coScene-logo").click()
            page.wait_for_timeout(1000)
            page.get_by_text("Bubbl自动化测试专属项目测试数据，勿动内部").first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="仪表盘").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="任务").click()
            page.wait_for_timeout(1000)
            page.get_by_text("通用任务").click()
            page.wait_for_timeout(1000)
            page.get_by_text("标注任务").click()
            page.wait_for_timeout(1000)
            page.get_by_text("采集任务").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="自动化").click()
            page.wait_for_timeout(1000)
            page.get_by_text("动作").click()
            page.wait_for_timeout(1000)
            page.get_by_text("触发器").click()
            page.wait_for_timeout(1000)
            page.get_by_text("调用历史").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="批量测试").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="数采&诊断").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="项目设备", exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="项目概览").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="项目设置").click()
            page.wait_for_timeout(1000)
            page.get_by_text("服务集成").click()
            page.wait_for_timeout(1000)
            page.get_by_text("可视化布局配置").click()
            page.wait_for_timeout(1000)
            page.get_by_text("基本设置").click()
            page.wait_for_timeout(1000)
            page.get_by_text("高级设置").click()
            page.wait_for_timeout(1000)
            page.get_by_role("link", name="coScene-logo").click()
            page.wait_for_timeout(1000)

        # 更多操作可以继续扩展
        # print("Test completed.")
        # browser.close()