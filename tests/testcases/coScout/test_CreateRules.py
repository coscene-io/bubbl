import re
import os
import allure
from playwright.sync_api import sync_playwright, expect



def Rule_group_name(file_path="counter.txt"):
    try:
        # 尝试读取计数器文件
        with open(file_path, "r") as file:
            counter = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        # 如果文件不存在或内容无效，从 1 开始
        counter = 1

    # 自增计数器并写回文件
    with open(file_path, "w") as file:
        file.write(str(counter + 1))

    return counter
@allure.story("Create rules and enable them")
def test_create_project_step_by_step():
    with sync_playwright() as playwright:
        # 启动浏览器
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        token = os.environ.get("JWT_TOKEN")

        if not token:
            raise ValueError("CN_JWT environment variable is not set")

        with allure.step("Set JWT in localStorage"):
            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
        # 打开页面
        page = context.new_page()
    # 项目和规则的参数化
        rule_num = Rule_group_name()
        project_name = "🅱️Bubbl自动化测试专属项目测试数据，勿动内部"
        rule_group = f"自动生成规则组{rule_num}"
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
                page.wait_for_selector(f"text={rule_num}")
                page.get_by_text(project_name).first.click()

            # Step 2: 进入数采&诊断页面
            with allure.step("进入数采&诊断页面"):
                page.get_by_role("button", name="数采&诊断").click()

            # Step 3: 添加规则组
            with allure.step("添加规则组"):
                page.get_by_role("button", name="添加规则组").click()
                page.wait_for_timeout(500)
                page.get_by_placeholder("输入记录名称").click()
                page.wait_for_timeout(500)
                page.get_by_placeholder("输入记录名称").fill(f"{rule_group}")
                page.wait_for_timeout(500)
                page.get_by_role("button", name="创建").click()
                page.wait_for_selector(f"text={rule_group}")
                page.get_by_text(rule_group).first.click()

            # Step 4: 创建规则
            with allure.step("创建规则"):
                page.get_by_role("button", name="创建空白规则").click()
                page.get_by_placeholder("未命名规则").fill(rule_name)
                page.locator("button").filter(has_text="选择话题").click()
                page.get_by_text(topic_name).click()

            # Step 5: 配置规则参数
            with allure.step("配置规则参数"):
                page.get_by_placeholder("设备消息字段，如 msg.message").fill(field_name)
                page.locator("div").filter(
                    has_text=re.compile(r"^事件匹配条件切换为代码模式包含事件码表 code 列任一行的值并且$")
                ).get_by_role("button").nth(2).click()
                page.get_by_placeholder("请输入具体值").fill(specific_value)
                page.get_by_label("诊断数据").check()

            # Step 6: 添加属性
            with allure.step("添加属性"):
                page.get_by_role("button", name="添加").click()
                page.get_by_placeholder("属性名称").fill(attribute_name)
                page.get_by_placeholder("属性值").fill(attribute_value)

            # Step 7: 设置布尔值并创建规则
            with allure.step("设置布尔值并创建规则"):
                page.locator("div").filter(has_text=re.compile(r"^是$")).click()
                page.get_by_label("是").click()
                page.get_by_role("button", name="创建", exact=True).click()
                page.wait_for_timeout(500)
                page.get_by_role("heading", name=rule_group).get_by_role("switch").click()
                page.wait_for_timeout(500)

            with allure.step("刷新当前页面"):
                page.reload()
                allure.attach(page.content(),name="刷新后页面内容",attachment_type=allure.attachment_type.HTML)
                page.wait_for_timeout(2000)

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