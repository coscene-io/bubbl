import re
import allure
from playwright.sync_api import sync_playwright, expect


@allure.story("通过 Token 登录，并按照步骤执行操作创建项目")
def test_create_project_step_by_step():
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
    # 项目和规则的参数化
        project_name = "🅱️Bubbl自动化测试专属项目测试数据，勿动内部"
        rule_group_name = "未命名规则组(0)"
        rule_name = "bag"
        topic_name = "/version"
        field_name = "msg.code"
        specific_value = "interactive"
        attribute_name = "等级"
        attribute_value = "{scope.level}"


        try:
            # Step 1: 选择项目
            with allure.step("选择项目"):
                page.goto("https://staging.coscene.cn/project-management")
                page.wait_for_selector(f"text={project_name}")
                page.get_by_text(project_name).first.click()
                # page.wait_for_timeout(1000)

            # Step 2: 进入数采&诊断页面
            with allure.step("进入数采&诊断页面"):
                # page.wait_for_selector("button[name='数采&诊断']")
                page.get_by_role("button", name="数采&诊断").click()
                # page.wait_for_timeout(1000)

            # Step 3: 添加规则组
            with allure.step("添加规则组"):
                page.get_by_role("button", name="添加规则组").click()
                page.get_by_role("button", name="创建").click()
                page.wait_for_selector(f"text={rule_group_name}")
                page.get_by_text(rule_group_name).first.click()
                # page.wait_for_timeout(1000)

            # Step 4: 创建规则
            with allure.step("创建规则"):
                page.get_by_role("button", name="创建空白规则").click()
                page.get_by_placeholder("未命名规则").fill(rule_name)
                page.locator("button").filter(has_text="选择话题").click()
                page.get_by_text(topic_name).click()
                # page.wait_for_timeout(1000)

            # Step 5: 配置规则参数
            with allure.step("配置规则参数"):
                page.get_by_placeholder("设备消息字段，如 msg.message").fill(field_name)
                page.locator("div").filter(
                    has_text=re.compile(r"^事件匹配条件切换为代码模式包含事件码表 code 列任一行的值并且$")
                ).get_by_role("button").nth(2).click()
                page.get_by_placeholder("请输入具体值").fill(specific_value)
                page.get_by_label("诊断数据").check()
                # page.wait_for_timeout(1000)

            # Step 6: 添加属性
            with allure.step("添加属性"):
                page.get_by_role("button", name="添加").click()
                page.get_by_placeholder("属性名称").fill(attribute_name)
                page.get_by_placeholder("属性值").fill(attribute_value)
                # page.wait_for_timeout(1000)

            # Step 7: 设置布尔值并创建规则
            with allure.step("设置布尔值并创建规则"):
                page.locator("div").filter(has_text=re.compile(r"^是$")).click()
                page.get_by_label("是").click()
                page.get_by_role("button", name="创建", exact=True).click()
                page.wait_for_timeout(1000)

            with allure.step("刷新当前页面"):
                page.reload()
                allure.attach(page.content(),name="刷新后页面内容",attachment_type=allure.attachment_type.HTML)
                page.wait_for_timeout(3000)

        except Exception as e:
            # 捕获异常并附加页面截图到 Allure 报告
            allure.attach(page.screenshot(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach(page.content(), name="Error Page Content", attachment_type=allure.attachment_type.HTML)
            raise e  # 重新抛出异常以便 pytest 处理

        finally:
            # 关闭浏览器资源
            if not page.is_closed():
                page.close()
            context.close()
            browser.close()