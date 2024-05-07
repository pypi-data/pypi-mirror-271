import time
from tabulate import tabulate


class TimedScope:
    def __init__(self, name: str, storage : dict):
        self.name : str = name
        self.storage : dict = storage

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed = end_time - self.start_time
        if self.name in self.storage:
            self.storage[self.name][0].append(elapsed)
            self.storage[self.name][1] += 1
        else:
            self.storage[self.name] = [[elapsed], 1]

class Profilable:
    def __init__(self):
        self._execution_times = {}

    def make_report(self) -> str:
        headers = ["Section", "Total Time (s)", "Average Time (s)", "Calls"]
        table = []
        for section, (times, calls) in self._execution_times.items():
            total_time = sum(times)
            average_time = total_time / calls
            table.append([section, f"{total_time:.6f}", f"{average_time:.6f}", calls])
        return tabulate(table, headers=headers, tablefmt="psql")

    def timed_scope(self, name : str) -> TimedScope:
        return TimedScope(name, self._execution_times)


class ExampleClass(Profilable):
    def some_method(self):
        with self.timed_scope(name='being_work'):
            time.sleep(0.1)
        with self.timed_scope(name='phase2'):
            time.sleep(0.1)
        with self.timed_scope(name='phase3'):
            time.sleep(0.1)

if __name__ == "__main__":
    instance = ExampleClass()
    instance.some_method()  # Execute the profiled method multiple times to see accumulation
    instance.some_method()
    print(instance.make_report())  # Output the profiling report
