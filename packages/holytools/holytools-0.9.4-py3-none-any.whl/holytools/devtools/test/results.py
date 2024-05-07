import os
import time
import traceback
import unittest
import linecache
from dataclasses import dataclass
from typing import Optional
from unittest import TestCase

from holytools.logging import LogLevel, CustomLogger
from .configurable_unit import ConfigurableTest
from .cases import ReportableResult, CaseReport, CaseStatus, get_case_name

# ---------------------------------------------------------

@dataclass
class DisplayOptions:
    show_runtimes : bool =True
    show_details : bool = True


class Results(ReportableResult):
    def __init__(self, logger : CustomLogger, settings : DisplayOptions, manual_mode : bool = False, *args, **kwargs):
        kwargs['logger'] = logger
        super().__init__(*args, **kwargs)
        self.test_settings : DisplayOptions = settings
        self.start_times : dict[str, float] = {}
        self.is_manual : bool = manual_mode
        self.print_header(f'  Test suite for \"{self.__class__.__name__}\"  ')

    def stopTestRun(self):
        super().stopTestRun()
        self.print_summary()

    def startTest(self, test : ConfigurableTest):
        if self.is_manual:
            test.set_manual()
        self.log(msg=f'------> {get_case_name(test=test)[:self.test_spaces]} ', level=LogLevel.INFO)
        self.start_times[test.id()] = time.time()
        super().startTest(test)

    # ---------------------------------------------------------
    # case logging

    def report(self, test : TestCase, status: CaseStatus, err : Optional[tuple] = None):
        case_result = CaseReport(test=test, status=status, runtime=self.get_runtime(test=test))
        self.case_results.append(case_result)

        conditional_err_msg = f'\n{self.get_err_details(err)}' if err and self.test_settings.show_details else ''
        finish_log_msg = f'Status: {status.value}{conditional_err_msg}\n'
        self.log(msg=finish_log_msg, level=status.get_log_level())


    @staticmethod
    def get_err_details(err) -> str:
        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)

        def is_relevant(tb):
            not_unittest = not os.path.dirname(unittest.__file__) in tb.filename
            not_custom_unittest = not os.path.dirname(__file__) in tb.filename
            return not_unittest and not_custom_unittest

        relevant_tb = [tb for tb in tb_list if is_relevant(tb)]

        result = ''
        for frame in relevant_tb:
            file_path = frame.filename
            line_number = frame.lineno
            tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}')
            result += f'{err_class.__name__}: {err_instance}\n{tb_str}'
        return result


    def get_runtime(self, test : TestCase) -> Optional[float]:
        test_id = test.id()
        if test_id in self.start_times:
            time_in_sec =  time.time() - self.start_times[test_id]
            return round(time_in_sec, 3)
        else:
            self.log(f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}', level=LogLevel.ERROR)

    # ---------------------------------------------------------
    # summary logging

    def print_summary(self):
        self.print_header(msg=' Summary ', seperator='-')
        for case in self.case_results:
            level = case.status.get_log_level()
            name_msg = f'{case.name[:self.test_spaces - 4]:<{self.test_spaces}}'
            status_msg = f'{case.status.value:<{self.status_spaces}}'
            runtime_str = f'{case.runtime_sec}s'
            runtime_msg = f'{runtime_str:^{self.runtime_space}}' if self.test_settings.show_runtimes else ''

            self.log(f'{name_msg}{status_msg}{runtime_msg}', level=level)
        self.log(self.get_final_status())
        self.print_header(msg='')


    def print_header(self, msg: str, seperator : str = '='):
        total_len = self.test_spaces + self.status_spaces
        total_len += self.runtime_space if self.test_settings.show_runtimes else 0
        line_len = max(total_len- len(msg), 0)
        lines = seperator * int(line_len / 2.)
        self.log(f'{lines}{msg}{lines}')


    def get_final_status(self) -> str:
        num_total = self.testsRun
        num_unsuccessful = len(self.errors)+ len(self.failures)

        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        CHECKMARK = '✓'
        CROSS = '❌'

        if num_unsuccessful == 0:
            final_status = f"{GREEN}\n{CHECKMARK} {num_total}/{num_total} tests ran successfully!{RESET}"
        else:
            final_status = f"{RED}\n{CROSS} {num_unsuccessful}/{num_total} tests had errors or failures!{RESET}"

        return final_status

