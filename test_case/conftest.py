import pytest
import requests

from utils.logger_util import LogUtil
from utils.request_util import RequestUtil
from utils.yaml_util import read_config_yaml

logger = LogUtil()


@pytest.fixture(autouse=True, scope="session")
def http_session():
    headers = read_config_yaml(read_config_yaml("env"), "base_config", "headers")
    logger.debug(f"从config.yaml文件中读取到的headers:{headers}")
    session = RequestUtil().session
    session.headers.update(headers)
    logger.debug(f"session.headers:{session.headers}")
    yield session
    session.close()


@pytest.fixture(scope="session")
def api_deps():
    """存储接口依赖字段的全局字典（如token、user_id等）"""
    return {}