import re
import time
import allure
import logging
import paramiko
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright  # 使用 Playwright 进行 UI 自动化

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

#创建项目&规则自增1
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

# 虚拟机SSH配置（根据实际信息修改）
host = "172.17.0.1"
port = 22
username = "just2004noetic"
password = "123456"  # SSH 密码
sudo_password = "123456"  # sudo 密码


# 获取当前时间（UTC+8）
current_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%y%m%d-%H%M%S")

# 第一个要执行的命令（卸载）
uninstall_command = f'echo "{sudo_password}" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/uninstall.sh)"'

# 第二个要执行的命令（安装），动态生成 --serial_num 参数
install_command = (
    f'echo "{sudo_password}" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/v2/install-beta.sh)" '
    f'-s --mod="default" --org_slug="coscene-lark" --server_url="https://openapi.staging.coscene.cn" '
    f'--coLink_endpoint="https://coordinator.staging.coscene.cn/api" --coLink_network="cf746e23-3210-4b8f-bdfa-fb771d1ac87c" '
    f'--serial_num="{current_time}" --remove_config --beta'
)

def execute_command(ssh_client, command):
    logging.info("正在执行以下命令：")
    logging.info(command)

    try:
        # 执行命令
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # 读取输出和错误信息
        output = stdout.read().decode()
        error = stderr.read().decode()

        logging.info("命令输出：\n%s", output)
        if error:
            logging.error("错误信息：\n%s", error)

        # 检查命令是否成功执行
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logging.info("命令成功执行")
            return True
        else:
            logging.error("命令执行失败，退出状态：%s", exit_status)
            return False

    except Exception as e:
        logging.error("命令执行失败: %s", e)
        return False

def ssh_operations():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        logging.info("尝试连接到 SSH 主机：%s", host)
        ssh.connect(host, port, username, password)

        # 执行第一个命令（卸载）
        if execute_command(ssh, uninstall_command):
            logging.info("卸载命令已成功执行，准备执行安装命令...")
            # 执行第二个命令（安装）
            return execute_command(ssh, install_command)
        else:
            logging.error("卸载命令执行失败，安装命令不会被执行。")
            return False

    except Exception as e:
        logging.error("SSH 连接失败: %s", e)
        return False
    finally:
        ssh.close()

def token_login():
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
        page.goto("https://staging.coscene.cn/")

        with allure.step("点击新建项目"):
            page.get_by_role("button", name="新建项目").click()
            page.wait_for_timeout(1000)
            logging.info("点击新建项目")

        with allure.step("选择项目模版"):
            page.get_by_label("选择项目模版").click()
            page.wait_for_timeout(1000)
            logging.info("选择项目模板")

        with allure.step("创建项目"):
            page.locator("div").filter(has_text=re.compile(r"^推荐新建空白项目$")).get_by_role("img").click()
            page.wait_for_timeout(1000)
            logging.info("创建项目")

        with allure.step("输入项目名称"):
            project_number = get_and_increment_counter()
            page.get_by_placeholder("输入项目名称").fill(f"创建新项目{project_number}")
            page.wait_for_timeout(1000)
            page.get_by_placeholder("输入项目网址").click()
            page.get_by_placeholder("输入项目网址").fill(f"cjxxm{project_number}")
            page.wait_for_timeout(500)
            logging.info("输入项目名称")

        with allure.step("创建项目完成"):
            page.get_by_role("button", name="完成创建").click()
            page.wait_for_timeout(1000)
            logging.info("创建项目完成")

        with allure.step("进入数采&诊断页面"):
            page.get_by_role("button", name="数采&诊断").click()

        with allure.step("添加规则组"):
            rule_num = get_and_increment_counter()
            logging.info("添加规则组")
            rule_group = f"自动生成规则组{rule_num}"
            page.get_by_role("button", name="添加规则组").click()
            page.wait_for_timeout(500)
            page.get_by_placeholder("输入记录名称").click()
            page.wait_for_timeout(500)
            page.get_by_placeholder("输入记录名称").fill(f"{rule_group}")
            page.wait_for_timeout(500)
            page.get_by_role("button", name="创建").click()
            page.wait_for_selector(f"text={rule_group}")
            page.get_by_text(rule_group).first.click()

        with allure.step("创建规则"):
            rule_name = "bag"
            topic_name = "/version"
            logging.info("创建规则")
            page.get_by_role("button", name="创建空白规则").click()
            page.get_by_placeholder("未命名规则").fill(rule_name)
            page.locator("button").filter(has_text="选择话题").click()
            page.get_by_text(topic_name).click()

        with allure.step("配置规则参数"):
            field_name = "msg.code"
            specific_value = "interactive"
            page.get_by_placeholder("设备消息字段，如 msg.message").fill(field_name)
            page.locator("div").filter(
                has_text=re.compile(r"^事件匹配条件切换为代码模式包含事件码表 code 列任一行的值并且$")
            ).get_by_role("button").nth(2).click()
            page.get_by_placeholder("请输入具体值").fill(specific_value)
            page.get_by_label("诊断数据").check()

        with allure.step("添加属性"):
            attribute_name = "等级"
            attribute_value = "{scope.level}"
            page.get_by_role("button", name="添加").click()
            page.get_by_placeholder("属性名称").fill(attribute_name)
            page.get_by_placeholder("属性值").fill(attribute_value)

        with allure.step("设置布尔值并创建规则"):
            page.locator("div").filter(has_text=re.compile(r"^是$")).click()
            page.get_by_label("是").click()
            page.get_by_role("button", name="创建", exact=True).click()
            page.wait_for_timeout(500)
            page.get_by_role("heading", name=rule_group).get_by_role("switch").click()
            page.wait_for_timeout(500)
            logging.info("创建规则成功")

        with allure.step("刷新当前页面"):
            page.reload()
            allure.attach(page.content(), name="刷新后页面内容", attachment_type=allure.attachment_type.HTML)
            page.wait_for_timeout(1000)

        with allure.step("启用客户端并添加设备到项目"):
            page.get_by_role("link", name="coScene-logo").click()
            page.wait_for_timeout(500)

            page.get_by_text("前往组织管理").click()
            page.wait_for_timeout(500)
            logging.info("前往组织管理")

            page.get_by_role("button", name="设备").click()
            page.wait_for_timeout(500)
            logging.info("进入设备页")

            page.get_by_role("button", name="启用客户端").first.click()
            logging.info("点击 '启用客户端' 按钮")
            page.wait_for_timeout(500)

            page.get_by_role("row", name=f"{current_time} {current_time}").get_by_label("").check()
            logging.info("选择客户端行：%s", current_time)
            page.wait_for_timeout(500)

            page.get_by_role("button", name="添加关联项目").click()
            logging.info("点击 '添加关联项目' 按钮")
            page.wait_for_timeout(1000)

            page.get_by_role("combobox").click()
            logging.info("点击下拉框选择项目")
            page.wait_for_timeout(1000)

            page.get_by_text("规则简化专用项目").click()
            logging.info("选择项目 '规则简化专用项目'")
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="添加").click()
            logging.info("点击 '添加' 按钮")
            page.wait_for_timeout(1000)
            page.reload()
            allure.attach(page.content(), name="刷新后页面内容", attachment_type=allure.attachment_type.HTML)
            page.wait_for_timeout(3000)
            browser.close()
            logging.info("所有操作已完成，浏览器已关闭")

def main():
    logging.info("开始执行卸载&添加设备命令")
    # 先执行 SSH 操作
    if ssh_operations():
        logging.info("SSH 操作完成，等待 5 秒后执行自动化操作...")
#        time.sleep(5)  # 停顿 5 秒
        for i in range(5, 0, -1):
            logging.info(f" {i} ...")
            time.sleep(1)
        logging.info("开始登录并执行后续操作...")
        token_login()
    else:
        logging.error("SSH 操作未成功，跳过自动化操作。")

# 调用主函数
if __name__ == "__main__":
    main()