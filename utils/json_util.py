import json
import os

from utils.constants import CaseType
from utils.get_fun_util import GetFunUtil
from utils.logger_util import LogUtil
from utils.shell_util import ShellUtil

logger = LogUtil()


def get_project_path():
    return os.path.dirname(os.path.dirname(__file__))


def read_json(fp, case_type=None):
    try:
        fp = os.path.join(get_project_path(), fp)
        with open(fp) as f:
            value = json.load(f)
            '''筛选出符合type的测试用例'''
            # 如果case_type传了参并且不是all,那么就筛选
            if case_type is not None and case_type != CaseType.ALL.value:
                value = [case for case in value if case.get("type") == case_type]
        return value
    except Exception as e:
        logger.debug(e)


def convert_to_int(s, key):
    # isdigit()方法检测字符串是否只由数字组成，只对0和正数有效
    if s.isdigit() and key in ['id', 'map_id', 'mapId', "map_name"]:
        return int(s)
    else:
        return s


def convert_json(json_obj, case_path):
    """
    解析测试用例json中的函数和sql
    :param json_obj:字典 {'title': '正常重命名分支', 'data': {'new_name': 'my_renamed_branch'}, 'type': 'normal'}
    :param case_path:
    :return:
    """
    try:
        data = json_obj["data"]
        # 如果请求数据为空,直接返回data对象
        if not data:
            return data
        # 1获取所有key
        all_keys = get_all_keys(data)
        # 2遍历所有key
        for key in all_keys:
            # 3如果key在业务范围内
            if key in ['id', 'map_id', 'path_id', 'map_name']:
                # 4 取key对应的values
                values = get_key_values(data, key)
                # 5 遍历values
                for i in range(len(values)):
                    v = values[i]
                    # 如果是字符串，且以get_fun_或者select开头，那么需要解析字符串为执行结果值
                    if isinstance(v, str):
                        if v.startswith("get_fun_"):
                            fun_v = eval(f"GetFunUtil.{v}")
                            logger.debug(f"解析结果是{fun_v}")
                            ReplaceJsonKey().replace_json_key(data, key, fun_v, i)
                        elif v.startswith("select "):
                            sql_v = convert_to_int(ShellUtil().ssh_sql(v), key)
                            logger.debug(f"解析结果是{sql_v}")
                            ReplaceJsonKey().replace_json_key(data, key, sql_v, i)
        return json_obj

    except Exception as e:
        logger.debug(f"{case_path}中的文件函数/sql解析失败{e}")


def get_all_keys(json_obj, results=None):
    """
    将一个json对象所有的key去重后放在列表中返回
    :param json_obj:json对象
    :param results: 获取到的返回结果，放在参数中是为了防止递归时丢失数据
    :return:
    """
    try:
        '''如果是默认传参空，初始化为空列表'''
        if results is None:
            results = []
        if json_obj:
            '''如果是字典，results加key,继续递归v,因为v可能是嵌套字典'''
            '''如果是列表，递归遍历每一个列表的元素，因为该元素也有可能是嵌套的字典'''
            if isinstance(json_obj, dict):
                for k, v in json_obj.items():
                    results.append(k)
                    get_all_keys(v, results)
            elif isinstance(json_obj, list):
                for i in json_obj:
                    get_all_keys(i, results)
        return list(set(results))
    except Exception as e:
        logger.debug(e)


def get_key_values(data, key, results=None):
    '''
    遍历多层嵌套的 JSON 格式数据（字典、列表 / 元组），
    查找指定键（key）对应的所有值（value）；若存在重名的 key，会将所有匹配的 value 收集到列表中返回。
    :param data: JSON 格式数据（字典、列表 / 元组）
    :param key:指定键（key
    :param results: 指定键（key）对应的所有值（value）；若存在重名的 key，会将所有匹配的 value 收集到列表中返回。
    :return:
    '''
    try:
        if results is None:
            results = []
        if data:
            if isinstance(data, dict):
                for k, v in data.items():
                    if k == key:
                        results.append(v)
                    get_key_values(v, key, results)
            elif isinstance(data, list):
                for i in data:
                    get_key_values(i, key, results)
        return results
    except Exception as e:
        logger.debug(e)


class ReplaceJsonKey:
    def __init__(self):
        self.p = 0

    def replace_json_key(self, data, key, value, index):
        """
        递归遍历嵌套的 JSON 数据结构（字典 / 列表 / 元组）
        ，找到指定名称的节点（key），并替换第 N 个（由 index 指定）匹配节点的值为新值
        :param data:json对象
        :param key:指定名称的节点（key）
        :param value:
        :param index:
        :return:
        """
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    if self.p == index:
                        data[k] = value
                        self.p += 1
                    else:
                        self.p += 1
                elif isinstance(v, dict):
                    self.replace_json_key(v, key, value, index)
                elif isinstance(v, list):
                    for i in v:
                        self.replace_json_key(i, key, value, index)
        elif isinstance(data, list):
            for i in data:
                self.replace_json_key(i, key, value, index)
        return data


if __name__ == "__main__":
    cases = {"title": "正常重命名分支", "data": {"new_name": "my_renamed_branch", "map_name": "get_fun_date()",
                                                 "id": "select id from map where name ='预置地图_pre';"},
             "type": "normal"}

    # print(ReplaceJsonKey().replace_json_key(case, "x", 555, 0))
    print(convert_json(cases, os.path.join(get_project_path(), "data", "branch", "rename_branch_cases.json")))
