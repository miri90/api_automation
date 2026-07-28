import io
import os.path
import sys
from datetime import datetime

import allure
from loguru import logger

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class AllureSink:
    def write(self, message: str) -> None:
        try:
            # 每条日志附件带精确时间戳，方便区分
            log_time = datetime.now().strftime("%H:%M:%S.%f")
            allure.attach(
                body=message,
                name=f"log_{log_time}",
                attachment_type=allure.attachment_type.TEXT
            )

        except KeyError:
            # 当前无运行中的allure测试用例，直接忽略，不抛异常
            return


class LogUtil:
    __instance = None

    def __new__(cls):
        """
        继承魔术方法，实现单例logger
        """
        """首先创建log/2026-07-16目录"""
        # 定义log子目录名
        log_name = datetime.now().strftime("%Y-%m-%d")
        # 获取当前项目所在目录
        project_name = "api_automation"
        project_path = os.path.dirname(__file__).split(project_name)[0]
        # 创建目录名称
        log_path = os.path.join(project_path, project_name, "logs", log_name)
        # 判断目录是否存在，不存在则创建
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logger.remove()
        logger.add(sink=sys.stderr, level="DEBUG")
        logger.add(sink=os.path.join(log_path, "debug.log"), level="DEBUG", enqueue=True, rotation="5 MB",
                   retention="1 week")
        logger.add(sink=os.path.join(log_path, "info.log"), level="INFO", enqueue=True, rotation="5 MB",
                   retention="1 week")
        logger.add(sink=os.path.join(log_path, "warning.log"), level="WARNING", enqueue=True, rotation="5 MB",
                   retention="1 week")
        logger.add(sink=os.path.join(log_path, "error.log"), level="ERROR", enqueue=True, rotation="5 MB",
                   retention="1 week")
        logger.add(sink=os.path.join(log_path, "critical.log"), level="CRITICAL", enqueue=True, rotation="5 MB",
                   retention="1 week")

        # 3. Allure报告日志接收器（同步，禁止enqueue，否则线程丢失用例上下文）
        logger.add(
            sink=AllureSink(),
            level="DEBUG",
            enqueue=False
        )

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def debug(self, msg):
        logger.opt(depth=1).debug(msg)

    def info(self, msg):
        return logger.opt(depth=1).info(msg)

    def warning(self, msg):
        return logger.opt(depth=1).warning(msg)

    def error(self, msg):
        return logger.opt(depth=1).error(msg)


if __name__ == "__main__":
    logger = LogUtil()
