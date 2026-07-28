import os

import allure
import pytest


from utils.assert_util import AssertUtil
from utils.json_util import read_json, convert_json
from utils.logger_util import LogUtil
from utils.request_util import  RequestUtil
from utils.yaml_util import read_config_yaml

logger = LogUtil()


@allure.epic("Pytest Api Automation Starter")
@allure.feature("branch")
@pytest.mark.business
class TestRenameBranch:
    """获取config.yaml 中的环境配置信息，如baseurl,headers"""
    base_url = read_config_yaml(read_config_yaml("env"), "base_config", "url")
    headers = read_config_yaml(read_config_yaml("env"), "base_config", "headers")
    """获取存储在json文件中的接口信息"""
    api_path = os.path.join("data", "branch", "rename_branch_api.json")
    api_info = read_json(api_path)
    url = base_url + api_info["path"]
    method = api_info["method"]
    """获取存储在json文件中的接口测试用例数据"""
    cases_path = os.path.join("data", "branch", "rename_branch_cases.json")
    '''从config.yaml中获取想要执行的测试用例数据类型：all/normal/exception'''
    case_type = read_config_yaml(read_config_yaml("env"), "case_type")
    cases = read_json(cases_path, case_type)

    @allure.story("rename branch")
    @pytest.mark.parametrize('case', cases)
    def test_rename_branch(self, case):
        """取测试用例名称，allure动态指定"""
        case = convert_json(case, self.cases_path)
        case_title = case.get("title")
        allure.dynamic.title(case_title)

        r=RequestUtil().send_request(method=self.method, url=self.url, playload=case["data"])
        AssertUtil.check_res(r,case,case_title)
