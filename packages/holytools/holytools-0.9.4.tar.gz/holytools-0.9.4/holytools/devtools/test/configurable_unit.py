import unittest


class ConfigurableTest(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.is_manual_mode : bool = False

    def set_manual(self):
        self.is_manual_mode = True

    def get_is_manual(self):
        return self.is_manual_mode