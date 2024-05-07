from enum import Enum

from unittest import TestCase, TestResult
from abc import abstractmethod
from typing import Optional
from holytools.logging import LogLevel, CustomLogger

# ---------------------------------------------------------


class CaseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"

    def get_log_level(self) -> LogLevel:
        status_to_logging = {
            CaseStatus.SUCCESS: LogLevel.INFO,
            CaseStatus.ERROR: LogLevel.CRITICAL,
            CaseStatus.FAIL: LogLevel.ERROR,
            CaseStatus.SKIPPED: LogLevel.INFO
        }
        return status_to_logging[self]

class CaseReport:
    def __init__(self, test : TestCase, status : CaseStatus, runtime : float):
        self.runtime_sec : float = runtime
        self.name : str = get_case_name(test)
        self.status : CaseStatus = status


class ReportableResult(TestResult):
    test_spaces = 50
    status_spaces = 10
    runtime_space = 10

    def __init__(self, logger : CustomLogger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_results : list[CaseReport] = []
        self.log = logger.log


    def addSuccess(self, test):
        super().addSuccess(test)
        self.report(test, CaseStatus.SUCCESS)

    def addError(self, test, err):
        super().addError(test, err)
        self.report(test, CaseStatus.ERROR, err)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.report(test, CaseStatus.FAIL, err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.report(test, CaseStatus.SKIPPED)

    # ---------------------------------------------------------
    # case logging

    @abstractmethod
    def report(self, test : TestCase, status : CaseStatus, err : Optional[tuple] = None):
        pass


def get_case_name(test: TestCase) -> str:
    full_test_name = test.id()
    parts = full_test_name.split('.')
    last_parts = parts[-2:]
    test_name = '.'.join(last_parts)
    return test_name