import re
import allure
from playwright.sync_api import sync_playwright, Page, expect


def get_and_increment_counter(file_path="counter.txt"):
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
@allure.feature("创建项目测试")
def test_example_with_token():
    with sync_playwright() as playwright:
        project_number = get_and_increment_counter()
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
        with allure.step("打开项目页面"):
            page.goto("https://staging.coscene.cn/")

        with allure.step("点击新建项目"):
            page.get_by_role("button", name="新建项目").click()
            page.wait_for_timeout(1000)

        with allure.step("选择项目模版"):
            page.get_by_label("选择项目模版").click()
            page.wait_for_timeout(1000)

        with allure.step("创建项目"):
            page.locator("div").filter(has_text=re.compile(r"^推荐新建空白项目$")).get_by_role("img").click()
            page.wait_for_timeout(1000)

        with allure.step("输入项目名称"):
            page.get_by_placeholder("输入项目名称").fill(f"脚本生成项目{project_number}")
            page.wait_for_timeout(1000)
            page.get_by_text(f"jbscxm{project_number}").click()
            page.wait_for_timeout(500)

        with allure.step("完成创建"):
            page.get_by_role("button", name="完成创建").click()
            page.wait_for_timeout(1000)

if __name__ == "__main__":
    test_example_with_token()