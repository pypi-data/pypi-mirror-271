from __future__ import annotations
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

@dataclass
class LogSettings:
    threshold: LogLevel = LogLevel.INFO
    log_fpath: Optional[str] = None
    timestamp: bool = True
    include_ms : bool = False
    include_call_location : bool = False


class LogTarget:
    FILE = "FILE"
    CONSOLE = "CONSOLE"

