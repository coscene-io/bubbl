import re
import time
import allure
import logging
import paramiko
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright


# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 虚拟机SSH配置（根据实际信息修改）
host = "172.17.0.1"
port = 22
username = "just2004noetic"
password = "123456"
sudo_password = "123456"

# 创建项目&规则自增1
def get_and_increment_counter(file_path="counter.txt"):
    try:
        with open(file_path, "r") as file:
            counter = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        counter = 1

    with open(file_path, "w") as file:
        file.write(str(counter + 1))
    return counter

@allure.story("Step 1: 登录并创建项目")
def create_project():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            jwt_token = "Basic YXBpa2V5OllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="

            if not jwt_token:
                logger.error("JWT Token 未设置")
                return False

            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)
            page = context.new_page()
            project_number = get_and_increment_counter()

            page.goto("https://staging.coscene.cn/")

            page.get_by_role("button", name="新建项目").click()
            page.wait_for_timeout(1000)

            page.get_by_label("选择项目模版").click()
            page.wait_for_timeout(1000)

            page.locator("div").filter(has_text=re.compile(r"^推荐新建空白项目$")).get_by_role("img").click()
            page.wait_for_timeout(1000)

            page.get_by_placeholder("输入项目名称").fill(f"脚本生成项目{project_number}")
            page.wait_for_timeout(500)

            page.get_by_role("button", name="完成创建").click()
            page.wait_for_timeout(1000)

            logger.info(f"项目创建成功: 脚本生成项目{project_number}")
            return True
    except Exception as e:
        logger.error(f"创建项目失败: {e}")
        return False

@allure.story("Step 2: 创建规则")
def create_rule():
    try:
        rule_num = get_and_increment_counter()
        rule_group = f"自动生成规则组{rule_num}"
        rule_name = "bag"
        topic_name = "/version"
        field_name = "msg.code"
        specific_value = "interactive"
        attribute_name = "等级"
        attribute_value = "{scope.level}"

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            jwt_token = "Your_JWT_Token"

            context.add_init_script(f"""
                localStorage.setItem('coScene_org_jwt', '{jwt_token}');
                localStorage.setItem('i18nextLng', 'cn');
            """)

            page = context.new_page()
            page.goto("https://staging.coscene.cn/project-management")
            page.get_by_text("🅱️Bubbl").first.click()

            page.get_by_role("button", name="数采&诊断").click()
            page.get_by_role("button", name="添加规则组").click()

            page.get_by_placeholder("输入记录名称").fill(rule_group)
            page.get_by_role("button", name="创建").click()
            page.get_by_text(rule_group).first.click()

            page.get_by_role("button", name="创建空白规则").click()
            page.get_by_placeholder("未命名规则").fill(rule_name)
            page.locator("button").filter(has_text="选择话题").click()
            page.get_by_text(topic_name).click()

            page.get_by_placeholder("设备消息字段，如 msg.message").fill(field_name)
            page.get_by_placeholder("请输入具体值").fill(specific_value)
            page.get_by_label("诊断数据").check()

            page.get_by_role("button", name="添加").click()
            page.get_by_placeholder("属性名称").fill(attribute_name)
            page.get_by_placeholder("属性值").fill(attribute_value)

            page.get_by_label("是").click()
            page.get_by_role("button", name="创建", exact=True).click()

            logger.info(f"规则组和规则创建成功: {rule_group}")
            return True
    except Exception as e:
        logger.error(f"创建规则失败: {e}")
        return False

@allure.story("Step 3: SSH 操作")
def ssh_operations():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        current_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%y%m%d-%H%M%S")
        uninstall_command = f'echo "{sudo_password}" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/uninstall.sh)"'
        install_command = (
            f'echo "{sudo_password}" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/v2/install.sh)" '
            f'-s --mod="default" --org_slug="coscene-lark" --server_url="https://openapi.staging.coscene.cn" '
            f'--coLink_endpoint="https://coordinator.staging.coscene.cn/api" --coLink_network="cf746e23-3210-4b8f-bdfa-fb771d1ac87c" '
            f'--serial_num="{current_time}" --remove_config'
        )

        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(uninstall_command)
        if stdout.channel.recv_exit_status() != 0:
            logger.error("卸载命令执行失败")
            return False

        stdin, stdout, stderr = ssh.exec_command(install_command)
        if stdout.channel.recv_exit_status() != 0:
            logger.error("安装命令执行失败")
            return False

        logger.info("SSH 操作成功")
        return True
    except Exception as e:
        logger.error(f"SSH 操作失败: {e}")
        return False
    finally:
        ssh.close()

@allure.story("Step 4：Enable device")
def ui_operations():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)  # 如果需要可视化模式，设置 headless=False
        context = browser.new_context()
        # JWT Token 用于登录
        jwt_token = "Basic YXBpa2VjOllqRXlOMk0zWVRoaE5qQTBObVkyTXpGaE5Ea3lPR1F3WmpFMlpqVTFPREl3WVRZMU1XVmtZVFkwWkRka1lqVTBORFpqWVRnMVkyUXhZakV4WWpsallRPT0="
        if not jwt_token:
            raise ValueError("JWT Token 未设置")

        # 添加 JWT 到 localStorage
        logging.info("设置 JWT 到 localStorage...")
        context.add_init_script(f"""
            localStorage.setItem('coScene_org_jwt', '{jwt_token}');
            localStorage.setItem('i18nextLng', 'cn');
        """)

        # 打开页面并开始自动化操作
        page = context.new_page()
        page.wait_for_timeout(1500)
        page.goto("https://staging.coscene.cn/")
        page.wait_for_timeout(5000)

        current_time_max = ssh_operations.current_time
        try:
            # 模拟网页操作
            logging.info("启用客户端并添加项目...")
            page.get_by_text("前往组织管理").click()
            logging.info("点击 '前往组织管理' 按钮")
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="设备").click()
            logging.info("点击 '设备' 按钮")
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="启用客户端").first.click()
            logging.info("点击 '启用客户端' 按钮")
            page.wait_for_timeout(1000)

            page.get_by_role("row", name=f"{current_time_max} {current_time_max}").get_by_label("").check()
            logging.info("选择客户端行：%s", current_time_max)
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="添加关联项目").click()
            logging.info("点击 '添加关联项目' 按钮")
            page.wait_for_timeout(1000)

            page.get_by_role("combobox").click()
            logging.info("点击下拉框选择项目")
            page.wait_for_timeout(1000)

            page.get_by_text("🅱️Bubbl").click()
            logging.info("选择项目 '🅱️Bubbl'")
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="添加").click()
            logging.info("点击 '添加' 按钮")
        finally:
            browser.close()
            logging.info("浏览器已关闭")
@allure.story("主函数: 按步骤执行")
def main():
    if not create_project():
        logger.error("任务终止：创建项目失败")
        return

    if not create_rule():
        logger.error("任务终止：创建规则失败")
        return

    if not ssh_operations():
        logger.error("任务终止：SSH 操作失败")
        return
    if not ui_operations():
        logger.error("任务终止：启用并添加设备到项目失败")
        return

    logger.info("所有任务执行完成")

if __name__ == "__main__":
    main()