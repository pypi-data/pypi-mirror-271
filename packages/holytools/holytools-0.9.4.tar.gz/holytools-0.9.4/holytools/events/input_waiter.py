from typing import Any
from queue import Queue


class MatchesAny:
    def __eq__(self, other):
        return True


class InputWaiter:
    _any = MatchesAny()

    def __init__(self, target_value : Any = _any):
        self.q = Queue()
        self.target_value : Any = target_value
        self.is_done : bool = False

    def clear(self):
        self.q = Queue()

    def write(self, value):
        self.q.put(value)

    def get(self) -> Any:
        while True:
            value = self.q.get()
            if self.target_value == value:
                self.is_done = True
                return value

if __name__ == "__main__":
    waiter = InputWaiter(target_value=None)