import allure
from jsonschema.validators import validate

from utils.logger_util import LogUtil
from utils.yaml_util import read_config_yaml

logger = LogUtil()


class AssertUtil:
    @staticmethod
    def check_response_time(res, title):
        """对接口响应时间断言"""
        expected = read_config_yaml(read_config_yaml("env"), "total_seconds")
        if expected is None:
            logger.debug( f"{title} 未配置 total_seconds，跳过响应时间断言")
            return
        actual = res.elapsed.total_seconds()
        with allure.step(f"校验响应时间是否超过预期响应时间{expected}"):
            assert actual <= expected, f"断言失败，实际响应时间超限，实际响应时间{actual}s,最大限制时间{expected}s"


    @staticmethod
    def check_status_code(res, case, title):
        """对状态码进行断言"""
        expected = case.get("expected",{}).get("status_code")
        if expected is None:
            logger.debug(f"{title} 未配置 expected.status_code，跳过状态码断言")
            return
        actual = res.status_code
        logger.debug(f"response.status_code是{actual}") # int
        with allure.step(f"校验状态码是否为{expected}"):
            assert actual == expected, f"断言失败，实际状态码{actual},预期状态码{expected}"


    @staticmethod
    def check_json_body(res, case, title):
        expected_schema = case.get("expected",{}).get("schema")
        if expected_schema is None:
            logger.debug(f"{title} 未配置 expected.schema，跳过JSON响应体断言")
            return
        actual = res.json()
        with allure.step("断言响应体是否符合预期"):
            assert validate(instance=actual,
                            schema=expected_schema) is None, f"断言失败，实际响应体:{actual},不符合预期schema{expected_schema}"

    @staticmethod
    def check_res(res,case,title):
        """把异常处理统一到 check_res()"""
        try:
            AssertUtil.check_response_time(res, title)
            AssertUtil.check_status_code(res, case, title)
            AssertUtil.check_json_body(res, case, title)
        except Exception as e:
            logger.error(f"执行{title}用例时抛出异常{e}")
            assert False, f"执行{title}用例时抛出异常{e}"





if __name__=="__main__":
    try:
        1/0
    except Exception as e:
        logger.error(f"执行用例时抛出异常{e}")
        raise AssertionError(
            f"执行用例时抛出异常：{e}"
        ) from e