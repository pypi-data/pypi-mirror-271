from __future__ import annotations
import inspect
import logging
import sys
from typing import Union
from logging import Logger
from .log_settings import LogSettings, LogLevel, LogTarget
# ---------------------------------------------------------


class CustomLogger(logging.Logger):
    def log(self, msg : str, level : Union[int, LogLevel] = LogLevel.INFO, with_traceback : bool = False , *args, **kwargs):
        if isinstance(level, LogLevel):
            level = level.value
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame)[1]

        file_name = caller_frame.filename
        line_no = caller_frame.lineno

        extra_info = {Formatter.custom_file_name: file_name, Formatter.custom_line_no: line_no}
        super().log(msg=msg, level=level, extra=extra_info, exc_info = with_traceback, *args, **kwargs)


    def setLevel(self, level : Union[int, LogLevel]):
        if isinstance(level, LogLevel):
            level = level.value
        super().setLevel(level)


class LoggerFactory:
    _default_settings : LogSettings = LogSettings()


    @classmethod
    def set_defaults(cls, settings : LogSettings):
        cls._default_settings = settings

    @classmethod
    def make_logger(cls, name : str, settings : LogSettings) -> Logger:
        settings = settings or cls._default_settings

        logging.setLoggerClass(CustomLogger)
        # noinspection PyTypeChecker
        logger : CustomLogger = logging.getLogger(name=name)
        logging.setLoggerClass(Logger)
        logger.propagate = False
        logger.setLevel(settings.threshold)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.CONSOLE))
        logger.addHandler(stdout_handler)

        if settings.log_fpath:
            file_handler = logging.FileHandler(settings.log_fpath)
            file_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.FILE))
            logger.addHandler(file_handler)

        return logger


class Formatter(logging.Formatter):
    custom_file_name = 'custom_file_name'
    custom_line_no = 'custom_lineno'

    colors: dict = {
        logging.DEBUG: '\033[20m',
        logging.INFO: '\033[20m',
        logging.WARNING: '\033[93m',
        logging.ERROR: '\033[91m',
        logging.CRITICAL: '\x1b[31;1m'  # Bold Red
    }

    def __init__(self, settings : LogSettings, log_target : LogTarget):
        self.log_settings : LogSettings = settings
        self.log_target : LogTarget = log_target
        super().__init__()


    def format(self, record):
        log_fmt = "%(message)s"

        if self.log_settings.timestamp:
            custom_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            conditional_millis = f" {int(record.msecs)}ms" if self.log_settings.include_ms else ""
            timestamp = f"[{custom_time}{conditional_millis}]"
            log_fmt = f"{timestamp}: {log_fmt}"

        if self.log_settings.include_call_location:
            filename = getattr(record, Formatter.custom_file_name, record.filename)
            lineno = getattr(record, Formatter.custom_line_no, record.lineno)
            log_fmt += f" (\"{filename}:{lineno}\")"

        if self.log_target == LogTarget.CONSOLE:
            color_prefix = Formatter.colors.get(record.levelno, "")
            color_suffix = "\033[0m"
            log_fmt = color_prefix + log_fmt + color_suffix

        self._style._fmt = log_fmt
        return super().format(record)