from datetime import datetime
import time


class Timer:
    def __init__(self):
        self.start_time : datetime = datetime.now()

    def restart(self):
        self.start_time = datetime.now()

    def capture(self, verbose : bool = True) -> float:
        now = datetime.now()
        delta = now-self.start_time
        delta_sec = delta.total_seconds()
        if verbose:
            print(f'Time has been running for {delta_sec} seconds')
        return delta_sec

    @staticmethod
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{func.__name__}: Took {end_time - start_time} seconds to execute")
            return result

        return wrapper