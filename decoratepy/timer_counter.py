import time 
from .decorator import Decorator

class TimerCounter(Decorator):
    def __init__(self):
        super().__init__()
        self.initialize()

    @property
    def total_runtime(self) -> float:
        """
        Returns the total runtime in seconds.
        """
        return sum(self._timer[func_name] for func_name in self._timer.keys())

    @property
    def total_runcall(self) -> int:
        """
        Returns the total runcall.
        """
        return sum(self._counter[func_name] for func_name in self._counter.keys())

    def initialize(self) -> None:
        """
        Sets the timer and the counter to 0 for each functions.
        """
        self._timer = {}
        self._counter = {}

    def __repr__(self) -> str:
        """
        Returns the string representation.
        """
        string = "Timer(\n"
        for func_name in self._timer.keys():
            string += f"{func_name} : {self._counter[func_name]:4E} calls - {self._timer[func_name]:4E} seconds\n"
        string += f"-----------\ntotal runcall = {self.total_runcall} calls\ntotal runtime = {self.total_runtime:.4E} seconds"
        return string

    def wrapper(self, func, *args, **kwargs):
        """
        Runs the function with runtime measurement.
        """
        # Adding the name into the dictionnary.
        if func.__name__ not in self._timer.keys():
            self._timer[func.__name__] = 0
            self._counter[func.__name__] = 0
        # Runtime measurement.
        tic = time.time()
        outputs = func(*args, **kwargs)
        toc = time.time()
        self._timer[func.__name__] += toc - tic
        self._counter[func.__name__] += 1 
        # Return outputs of func.
        return outputs
