from .decorator import Decorator

class Counter(Decorator):
    def __init__(self):
        super().__init__()
        self.initialize()

    @property
    def total_runcall(self) -> int:
        """
        Returns the total runcall.
        """
        return sum(self._counter[func_name] for func_name in self._counter.keys())

    def initialize(self) -> None:
        """
        Sets the counter to 0 for each functions.
        """
        self._counter = {}

    def __repr__(self) -> str:
        """
        Returns the string representation.
        """
        string = "Counter(\n"
        for func_name in self._counter.keys():
            string += f"{func_name} : {self._counter[func_name]} calls\n"
        string += f"-----------\ntotal runcall = {self.total_runcall} calls"
        return string

    def wrapper(self, func, *args, **kwargs):
        """
        Runs the function with call counter.
        """
        # Adding the name into the dictionnary.
        if func.__name__ not in self._counter.keys():
            self._counter[func.__name__] = 0
        # Runcall measurement.
        outputs = func(*args, **kwargs)
        self._counter[func.__name__] += 1
        # Return outputs of func.
        return outputs
