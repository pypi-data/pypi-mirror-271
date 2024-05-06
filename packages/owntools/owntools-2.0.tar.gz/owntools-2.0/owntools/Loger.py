from loguru import logger
from pathlib import Path


class Logger():
    # 日志简单配置

    def __init__(self, logPath: str | Path, need_log=True,serialize=False):
        self.my_logger = logger

        # 判断是否需要写入日志
        if need_log is True:

            log_path = Path(logPath)

            if not log_path.parent.exists():
                Path.mkdir(log_path.parent, parents=True, exist_ok=True)

            _ = self.my_logger.add(log_path, retention="30 days", encoding='utf-8', enqueue=True,serialize=serialize)

    def info(self, content):

        self.my_logger.info(content)

    def debug(self, content):
        self.my_logger.debug(content)

    def error(self, content):
        self.my_logger.error(content)

    def critical(self, content):
        self.my_logger.critical(content)

    def warning(self, content):
        self.my_logger.warning(content)

    def success(self, content):
        self.my_logger.success(content)

    def trace(self, content):
        self.my_logger.trace(content)

    def traceback(self,content=""):
        self.my_logger.exception(content)
