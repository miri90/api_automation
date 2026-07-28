import os.path

import yaml

from utils.logger_util import LogUtil

logger = LogUtil()


def get_yaml_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


def read_yaml():
    """
    测试方法
    :return:
    """
    filename = get_yaml_path()
    with open(filename, mode="r", encoding="utf-8") as f:
        dict = yaml.load(f, Loader=yaml.SafeLoader)
    print(dict)
    # <class 'int'>
    print(type(dict[dict['env']]['base_config']['port']))
    # <class 'list'>
    print(type(dict['lst']))
    # <class 'bool'>
    print(type(dict['bool']))
    # <class 'NoneType'>
    print(type(dict['test']['server_info']['username']))


# def read_config_yaml(first_key, second_key=None, third_key=None, fourth_key=None):
#     """
#     :param first_key:
#     :param second_key:
#     :param third_key:
#     :param fourth_key:
#     :return:
#     """
#     file_name = get_yaml_path()
#     try:
#         with open(file_name) as f:
#             dict = yaml.load(f, yaml.SafeLoader) or {}
#             if second_key is None:
#                 return dict.get(first_key)
#             elif third_key is None:
#                 return dict.get(first_key) or {}.get(second_key)
#             elif fourth_key is None:
#                 return dict.get(first_key)or {}.get(second_key)or {}.get(third_key)
#             else:
#                 return dict.get(first_key) or {}.get(second_key)or {}.get(third_key) or {}.get(fourth_key)
#
#     except Exception as e:
#         logger.debug(e)


def read_config_yaml(*keys):
    """
    根据多个key读取YAML配置

    例如：
    read_config_yaml("env")
    read_config_yaml("env", "total_seconds")
    read_config_yaml("api", "github", "timeout")
    """

    file_name = get_yaml_path()

    try:
        with open(file_name, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        for key in keys:
            """为了防止传入的key值不存在"""
            if not isinstance(data, dict):
                return None

            data = data.get(key)

        return data

    except Exception as e:
        logger.error(
            f"读取YAML配置失败: {e}"
        )
        return None


if __name__ == "__main__":
    # print(get_yaml_path())
    # read_yaml()
    # logger.debug(read_config_yaml("test","base_config","url"))
    # logger.debug(read_config_yaml("env"))
    #
    v = "r" or {}
    dic = {
        "name": "max",
        "friend": {"name": "marc", "gender": "male"},
    }
    print(dic.get("sex"))
    print({} or None)
    print("" or None)
    read_config_yaml("test","server","headers","body")