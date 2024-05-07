import unittest

from typing import Optional
from holytools.logging import make_logger, LogSettings, CustomLogger, LogLevel
from .configurable_unit import  ConfigurableTest
from .results import Results, DisplayOptions

# ---------------------------------------------------------


class Runner(unittest.TextTestRunner):
    def __init__(self, logger : CustomLogger, settings : DisplayOptions, is_manual : bool = False):
        super().__init__(resultclass=None)
        self.logger : CustomLogger = logger
        self.display_options : DisplayOptions = settings
        self.manual_mode : bool = is_manual

    def run(self, test) -> Results:
        result = Results(logger=self.logger,
                         stream=self.stream,
                         settings=self.display_options,
                         descriptions=self.descriptions,
                         verbosity=2,
                         manual_mode=self.manual_mode)
        test(result)
        result.printErrors()

        return result


class Unittest(ConfigurableTest):
    _logger : CustomLogger = None

    @classmethod
    def execute_all(cls, manual_mode : bool = True, settings : DisplayOptions = DisplayOptions()):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(), settings=settings, is_manual=manual_mode)
        results =  runner.run(suite)
        results.print_summary()
        return results

    @classmethod
    def get_logger(cls) -> CustomLogger:
        if not cls._logger:
            cls._logger = make_logger(settings=LogSettings(include_call_location=False, timestamp=False), name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls, msg : str, level : LogLevel = LogLevel.INFO):
        cls.get_logger().log(f'--> {msg}', level=level)

    # ---------------------------------------------------------
    # assertions

    def assertEqual(self, first : object, second : object, msg : Optional[str] = None):
        if not first == second:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested expressions should match:'
                       f'\nFirst : {first_str}'
                       f'\nSecond: {second_str}')
            raise AssertionError(msg)


    def assertIn(self, member : object, container, msg : Optional[str] = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            if msg is None:
                msg = f'{member_str} not in {container_str}'
            raise AssertionError(msg)


    def assertIsInstance(self, obj : object, cls : type, msg : Optional[str] = None):
        if not isinstance(obj, cls):
            obj_str = str(obj).__repr__()
            cls_str = str(cls).__repr__()
            if msg is None:
                msg = f'{obj_str} not an instance of {cls_str}'
            raise AssertionError(msg)


    def assertTrue(self, expr : bool, msg : Optional[str] = None):
        if not expr:
            if msg is None:
                msg = f'Tested expression should be true'
            raise AssertionError(msg)


    def assertFalse(self, expr : bool, msg : Optional[str] = None):
        if expr:
            if msg is None:
                msg = f'Tested expression should be false'
            raise AssertionError(msg)


    def assertStrEqual(self, first : object, second : object, msg : Optional[str] = None):
        self.assertEqual(str(first), str(second), msg=msg)


    def assertRecursivelyEqual(self, first : dict, second : dict, msg : Optional[str] = None):
        for key in first:
            first_obj = first[key]
            second_obj = second[key]
            self.assertEqual(type(first_obj), type(second_obj))
            if isinstance(first_obj, dict):
                self.assertRecursivelyEqual(first_obj, second_obj, msg=msg)
            else:
                self.assertStrEqual(first[key], second[key])