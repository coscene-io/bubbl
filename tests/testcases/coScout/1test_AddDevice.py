import paramiko
from datetime import datetime, timedelta

# 虚拟机SSH配置（根据实际信息修改）
host = "192.168.1.85"
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
    print("正在执行以下命令：")
    print(command)

    try:
        # 执行命令
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # 读取输出和错误信息
        output = stdout.read().decode()
        error = stderr.read().decode()

        print("命令输出：\n", output)
        if error:
            print("错误信息：\n", error)

        # 检查命令是否成功执行
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("命令成功执行")
            return True
        else:
            print(f"命令执行失败，退出状态：{exit_status}")
            return False

    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)

        # 执行第一个命令（卸载）
        if execute_command(ssh, uninstall_command):
            print("卸载命令已成功执行，准备执行安装命令...")
            # 执行第二个命令（安装）
            execute_command(ssh, install_command)
        else:
            print("卸载命令执行失败，安装命令不会被执行。")

    except Exception as e:
        print(f"SSH 连接失败: {e}")
    finally:
        ssh.close()

# 调用主函数
main()