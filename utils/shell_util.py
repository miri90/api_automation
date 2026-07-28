import time

import paramiko

from utils.logger_util import LogUtil
from utils.yaml_util import read_config_yaml

logger = LogUtil()


class ShellUtil:
    hostname = read_config_yaml(read_config_yaml("env"), "server_info", "hostname")
    # port=read_config_yaml(read_config_yaml("env"),"server_info","port")
    username = read_config_yaml(read_config_yaml("env"), "server_info", "username")
    password = read_config_yaml(read_config_yaml("env"), "server_info", "password")

    @staticmethod
    def add_semicolon(s):
        if not s.endswith(";"):
            s += ";"
        return s

    def ssh_sql(self, command):
        # 拼接linux命令
        # chensiyue@magicBook ~ % sqlite3 database.db "select * from map;"
        command = f"""sqlite3 /Users/chensiyue/database.db "{ShellUtil.add_semicolon(command)}" """
        # 创建SSH对象
        client = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.hostname, username=self.username, password=self.password)
            stdin, stdout, stderr = client.exec_command(command)
            # 读取输出,字符串类型
            output = stdout.read().decode('utf-8').strip()
            # 等待命令执行完成(对于长时间运行的命令可能需要调整)
            time.sleep(3)  # 给命令一些时间开始执行
            results = []
            if output:
                results.append(output)
            # 将可迭代对象（这里是列表 re_data）中的所有元素拼接成一个字符串，
            # 拼接的分隔符是调用 join() 的字符串（这里是换行符 \n
            return "\n".join(results)
        except Exception as e:
            logger.debug(e)
        finally:
            client.close()


if __name__ == "__main__":
    print(ShellUtil().ssh_sql("select id from map where name ='预置地图_pre';"))
