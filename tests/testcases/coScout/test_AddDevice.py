import paramiko

# 虚拟机SSH配置（根据实际信息修改）
host = "192.168.1.85"
port = 22
username = "just2004noetic"
password = "123456"

# 要执行的命令字符串
#command = '/bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/uninstall.sh)"'
command = 'echo "123456" | sudo -S /bin/bash -c "$(curl -fsSL https://download.coscene.cn/coscout/v2/install.sh)" -s --mod="default" --org_slug="coscene-lark" --server_url="https://openapi.staging.coscene.cn" --coLink_endpoint="https://coordinator.staging.coscene.cn/api" --coLink_network="cf746e23-3210-4b8f-bdfa-fb771d1ac87c" --serial_num="250418-175956" --remove_config'

def execute_command(command):
    print("正在执行以下命令：")
    print(command)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)

        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)

        # 读取输出和错误信息
        output = stdout.read().decode()
        error = stderr.read().decode()

        print("命令输出：\n", output)
        if error:
            print("错误信息：\n", error)

    except Exception as e:
        print(f"连接失败: {e}")
    finally:
        ssh.close()

# 调用函数自动执行命令
execute_command(command)

