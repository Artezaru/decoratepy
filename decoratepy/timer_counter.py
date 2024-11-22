import time 
from .decorator import Decorator

class TimerCounter(Decorator):
    """
    Compute the number of call and runtime of various functions. 

    .. warning::
        If 2 functions/methods have the same '__name__' attribute, the TimerCounter will combined the two runtimes. 
    
    HELP TimerCounter
    =================
    
    Create a timer-counter with :

    .. code-block:: python

        timercounter = TimerCounter()

    Then decorate functions with the timer-counter. 

    .. code-block:: python

        @timercounter
        def func_name():
            pass

    Initialize and clear the timer-counter with : 

    .. code-block:: python

        timercounter = initialize()

    Use the functions and the timer-counter will compute number of calls and runtime.

    To deactivate and re-activate the timer-counter, use :

    .. code-block:: python

        timercounter.set_activated()
        timercounter.set_deactivated()

    Print the number of calls and runtimes with :
    
    .. code-block:: python

        print(timercounter.name_repr) # equivalent of print(timercounter)

    The result will be :
    
    .. code-block:: console
    
        TimerCounter(
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
        -----------
        total number of calls : {total_runcall}
        total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
        )
    """

    __help__ = """
HELP TimerCounter
=================

Create a timer-counter with :

.. code-block:: python

    timercounter = TimerCounter()

Then decorate functions with the timer-counter. 

.. code-block:: python

    @timercounter
    def func_name():
        pass

Initialize and clear the timer-counter with : 

.. code-block:: python

    timercounter = initialize()

Use the functions and the timer-counter will compute number of calls and runtime.

To deactivate and re-activate the timer-counter, use :

.. code-block:: python

    timercounter.set_activated()
    timercounter.set_deactivated()

Print the number of calls and runtimes with :

.. code-block:: python

    print(timercounter.name_repr) # equivalent of print(timercounter)

The result will be :

.. code-block:: console

    TimerCounter(
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    -----------
    total number of calls : {total_runcall}
    total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
    )
"""

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
        self._timer = {} # key: str = function name // value: float = runtime
        self._counter = {} # key: str = function name // value: int = number of call

    def __repr__(self) -> str:
        """
        Returns the string representation.
        Default = self.name_repr
        """
        return self.name_repr

    def _wrapper(self, func, *args, **kwargs):
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
    
    def get_help(self) -> str:
        """
        Returns the documentation 'How to Use' of the decorator
        """
        return self.__help__

    @property
    def name_repr(self) -> str:
        """
        Returns the string representation in the following format:
        
        .. code-block:: console
        
            TimerCounter(
            [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            -----------
            total number of calls : {total_runcall}
            total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
            )
        """
        string = "TimerCounter(\n"
        for func_name in self._timer.keys():
            # Conversion in hours, minutes, seconds.
            hours, remainder = divmod(self._timer[func_name], 3600)
            minutes, seconds = divmod(remainder, 60)
            string += f"[{func_name}] number of calls : {self._counter[func_name]} - cumulative runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
        # Adding total runtime and total call number.
        hours, remainder = divmod(self.total_runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        string += f"-----------\ntotal number of calls : {self.total_runcall}\ntotal runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n)"
        return string