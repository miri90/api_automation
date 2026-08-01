import os

import allure
import pytest

from utils.assert_util import AssertUtil
from utils.json_util import read_json, convert_json, extract_json_value, replace_variables
from utils.logger_util import LogUtil
from utils.request_util import RequestUtil
from utils.yaml_util import read_config_yaml
logger=LogUtil()



@allure.epic("Pytest Api Automation Starter")
@allure.feature("Issue")
@pytest.mark.business
class TestIssue:

    """获取config.yaml 中的环境配置信息，如baseurl,headers"""
    base_url = read_config_yaml(read_config_yaml("env"), "base_config", "url")
    headers = read_config_yaml(read_config_yaml("env"), "base_config", "headers")
    """获取存储在json文件中的接口信息"""
    create_issue_api_path = os.path.join("data", "issue", "create_issue_api.json")
    create_issue_api_info = read_json(create_issue_api_path)
    create_issue_url = base_url + create_issue_api_info["path"]
    create_issue_method = create_issue_api_info["method"]
    """获取存储在json文件中的接口测试用例数据"""
    create_issue_cases_path = os.path.join("data", "issue", "create_issue_cases.json")
    '''从config.yaml中获取想要执行的测试用例数据类型：all/normal/exception'''
    case_type = read_config_yaml(read_config_yaml("env"), "case_type")
    create_issue_cases = read_json(create_issue_cases_path, case_type)
    logger.debug(f"create an issue cases:{create_issue_cases}")

    """获取存储在json文件中的接口信息"""
    update_issue_api_path = os.path.join("data", "issue", "update_issue_api.json")
    update_issue_api_info = read_json(update_issue_api_path)
    update_issue_url = base_url + update_issue_api_info["path"]
    update_issue_method = update_issue_api_info["method"]
    """获取存储在json文件中的接口测试用例数据"""
    update_issue_cases_path = os.path.join("data", "issue", "update_issue_cases.json")
    update_issue_cases = read_json(update_issue_cases_path, case_type)
    logger.debug(f"update an issue cases:{update_issue_cases}")


    @allure.story("create issue")
    @pytest.mark.parametrize('case',create_issue_cases)
    @pytest.mark.order(1)
    def test_create_issue(self,case,api_deps):
        """取测试用例名称，allure动态指定"""
        case = convert_json(case, self.create_issue_cases_path)
        case_title = case.get("title")
        allure.dynamic.title(case_title)
        r = RequestUtil().send_request(method=self.create_issue_method, url=self.create_issue_url, playload=case["data"])
        AssertUtil.check_res(r, case, case_title)
        extract_json_value(r.json(),case,api_deps)
        logger.debug(f"api_deps变量池的变量：{api_deps}")

    @allure.story("update issue")
    @pytest.mark.parametrize('case', update_issue_cases)
    @pytest.mark.order(2)
    def test_update_issue(self, case, api_deps):
        """取测试用例名称，allure动态指定"""
        case = convert_json(case, self.update_issue_cases_path)
        case_title = case.get("title")
        allure.dynamic.title(case_title)
        """处理参数化的url,URL path 参数替换"""
        self.update_issue_url= replace_variables(self.update_issue_url, api_deps)
        r = RequestUtil().send_request(method=self.update_issue_method, url=self.update_issue_url,
                                       playload=case["data"])
        AssertUtil.check_res(r, case, case_title)
        extract_json_value(r.json(), case, api_deps)
        logger.debug(f"api_deps变量池的变量：{api_deps}")
