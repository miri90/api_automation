from unittest import case

import requests

from utils.logger_util import LogUtil
from utils.yaml_util import read_config_yaml

logger = LogUtil()


class RequestUtil:
    __instance = None
    session = None

    # 搞单例模式
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.session = requests.session()
        return cls.__instance

    def send_request(self, method, url, playload=None):
        try:
            if method == "get":
                r = self.session.get(url)
            elif method == "post":
                r = self.session.post(url, json=playload)

            logger.debug(f"接口url:{url}")
            logger.debug(f"接口请求头:{self.session.headers}")
            logger.debug(f"请求入参为:{playload}")
            logger.debug(f"响应体为:{r.json()}")
            return r
        except Exception as e:
            logger.error(f"调用{url}出错{e}")


if __name__ == "__main__":
    branch_name = "my_renamed_branch"
    headers = read_config_yaml(read_config_yaml("env"), "base_config", "headers")
    url = f"https://api.github.com/repos/miri90/wenda/branches/{branch_name}"
    response = requests.get(url, headers)
    # <class 'requests.models.Response'>
    print(type(response))
    print(response.status_code)
    # 返回json响应反序列化后的对象
    print(response.json())
    # 请求体会自动序列化为json字符串
    new_branch_name = "master"
    playload = {"new_name": branch_name}
    url = f"https://api.github.com/repos/miri90/wenda/branches/{new_branch_name}/rename"
    response = requests.post(url, headers=headers, json=playload)
    print(response.status_code)
    print(response.elapsed.total_seconds())
    print(response.json())
    requests.Session()
