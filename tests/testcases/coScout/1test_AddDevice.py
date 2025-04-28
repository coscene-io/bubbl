#!/usr/bin/env python3
import logging
import paramiko
import time
from playwright.sync_api import sync_playwright  # 使用 Playwright 进行 UI 自动化
from datetime import datetime, timedelta

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

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
    f'echo "{sudo_password}" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/v2/install.sh)" '
    f'-s --mod="default" --org_slug="coscene-lark" --server_url="https://openapi.staging.coscene.cn" '
    f'--coLink_endpoint="https://coordinator.staging.coscene.cn/api" --coLink_network="cf746e23-3210-4b8f-bdfa-fb771d1ac87c" '
    f'--serial_num="{current_time}" --remove_config'
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

            page.get_by_role("row", name=f"{current_time} {current_time}").get_by_label("").check()
            logging.info("选择客户端行：%s", current_time)
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
            page.wait_for_timeout(1000)
        finally:
            browser.close()
            logging.info("浏览器已关闭")

def main():
    logging.info("开始执行 SSH 和 UI 自动化脚本...")
    # 先执行 SSH 操作
    if ssh_operations():
        logging.info("SSH 操作完成，等待 5 秒后执行自动化操作...")
#        time.sleep(5)  # 停顿 5 秒
        for i in range(5, 0, -1):
            logging.info(f" {i} ...")
            time.sleep(1)
        # 执行 UI 自动化操作
        ui_operations()
    else:
        logging.error("SSH 操作未成功，跳过自动化操作。")

# 调用主函数
if __name__ == "__main__":
    main()