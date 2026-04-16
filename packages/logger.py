import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

from packages.configuration import DEBUG_IS, LOG_PATH, PROJECT_NAME
from packages.fs_operations import make_dest_dir

_is_debug = DEBUG_IS
_log_path = LOG_PATH
_log_name = PROJECT_NAME


class SecureRotatingFileHandler(RotatingFileHandler):
    def _open(self):
        fd = super()._open()
        os.chmod(self.baseFilename, 0o640)
        return fd


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if _is_debug:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

fmt = "%(asctime)s | %(levelname)8s | %(funcName)s | %(message)s"

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(loglevel)
stdout_handler.setFormatter(CustomFormatter(fmt))

today = datetime.date.today()

#Создать директорию для логов если таковая не имеется
make_dest_dir(_log_path, 0o750)
file_handler = SecureRotatingFileHandler(
    filename=f"{_log_path}/{_log_name}.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3,  # max backup count
    encoding="utf-8",
)
file_handler.setLevel(loglevel)
file_handler.setFormatter(logging.Formatter(fmt))

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
