import os

import allure
import pytest

from utils.assert_util import AssertUtil
from utils.json_util import read_json, convert_json, replace_variables
from utils.logger_util import LogUtil
from utils.request_util import RequestUtil
from utils.yaml_util import read_config_yaml

logger=LogUtil()

@allure.epic("Pytest Api Automation Starter")
@allure.feature("comment")
@pytest.mark.business
class TestComment:
    """获取config.yaml 中的环境配置信息，如baseurl,headers"""
    base_url = read_config_yaml(read_config_yaml("env"), "base_config", "url")
    headers = read_config_yaml(read_config_yaml("env"), "base_config", "headers")
    """获取存储在json文件中的接口信息"""
    api_path = os.path.join("data", "comment", "create_issue_comment_api.json")
    api_info = read_json(api_path)
    url = base_url + api_info["path"]
    method = api_info["method"]
    """获取存储在json文件中的接口测试用例数据"""
    cases_path = os.path.join("data", "comment", "create_issue_comment_cases.json")
    '''从config.yaml中获取想要执行的测试用例数据类型：all/normal/exception'''
    case_type = read_config_yaml(read_config_yaml("env"), "case_type")
    cases = read_json(cases_path, case_type)

    @allure.story("create an issue comment")
    @pytest.mark.parametrize('case', cases)
    @pytest.mark.order(3)
    def test_create_issue_comment(self, case,api_deps):
        logger.debug(f"when creating an issue comment，api_deps变量池的变量：{api_deps}")
        """对参数化get_fun_xx()/select/${}的json进行解析"""
        case = convert_json(case, self.cases_path,api_deps)
        """取测试用例名称，allure动态指定"""
        case_title = case.get("title")
        allure.dynamic.title(case_title)
        """对URL中的参数进行解析"""
        self.url=replace_variables(self.url,api_deps)
        r=RequestUtil().send_request(method=self.method, url=self.url, playload=case["data"])
        AssertUtil.check_res(r,case,case_title)
