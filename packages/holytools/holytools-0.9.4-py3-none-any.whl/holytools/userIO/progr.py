import progressbar
from progressbar import ProgressBar
# ---------------------------------------------------------

class TrackedInt:
    progressbar.streams.wrap_stderr()
    progressbar.streams.wrap_stdout()

    def __init__(self, start_value : int, max_value : int):
        self._value : int = start_value
        self.progressbar = ProgressBar(min_value=start_value, max_value=max_value)
        self.progressbar.update()

    def update(self, incr : int):
        self._value += incr

        if self.progressbar.finished():
            return

        if self._value >= self.progressbar.max_value:
            self.progressbar.finish()
            return

        self.progressbar.update(value=self._value)

    def get_value(self) -> int:
        return self._value

    def __iadd__(self, other):
        if not isinstance(other, int):
            raise ValueError("Only integers can be added to a TrackedInt.")
        self.update(incr=other)
        return self

    def __add__(self, other):
        raise NotImplementedError(f'Can only add to tracked integer in place')

    def __eq__(self, other):
        if isinstance(other, TrackedInt):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, TrackedInt):
            return self._value < other._value
        elif isinstance(other, int):
            return self._value < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, TrackedInt):
            return self._value <= other._value
        elif isinstance(other, int):
            return self._value <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, TrackedInt):
            return self._value > other._value
        elif isinstance(other, int):
            return self._value > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, TrackedInt):
            return self._value >= other._value
        elif isinstance(other, int):
            return self._value >= other
        return NotImplemented
