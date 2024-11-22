import time 
from .decorator import Decorator

class Timer(Decorator):
    """
    Compute the runtime of various functions. 

    .. warning::
        If 2 functions/methods have the same '__name__' attribute, the Timer will combined the two runtimes. 

    HELP Timer
    ============
    
    Create a timer with :

    .. code-block:: python

        timer = Timer()

    Then decorate functions with the timer. 

    .. code-block:: python

        @timer
        def func_name():
            pass

    Initialize and clear the timer with : 

    .. code-block:: python

        timer = initialize()

    Use the functions and the timer will compute runtimes.

    To deactivate and re-activate the timer, use :

    .. code-block:: python

        timer.set_activated()
        timer.set_deactivated()

    Print the runtimes with :
    
    .. code-block:: python

        print(timer.name_repr) # equivalent of print(timer)

    The result will be :
    
    .. code-block:: console
    
        Timer(
        [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
        -----------
        total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
        )
    """

    __help__ = """
HELP Timer
============

Create a timer with :

.. code-block:: python

    timer = Timer()

Then decorate functions with the timer. 

.. code-block:: python

    @timer
    def func_name():
        pass

Initialize and clear the timer with : 

.. code-block:: python

    timer = initialize()

Use the functions and the timer will compute runtimes.

To deactivate and re-activate the timer, use :

.. code-block:: python

    timer.set_activated()
    timer.set_deactivated()

Print the runtimes with :

.. code-block:: python

    print(timer.name_repr) # equivalent of print(timer)

The result will be :

.. code-block:: console

    Timer(
    [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
    -----------
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

    def initialize(self) -> None:
        """
        Sets the timer to 0 for each functions.
        """
        self._timer = {} # key: str = function name // value: float = runtime

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
        # Runtime measurement.
        tic = time.time()
        outputs = func(*args, **kwargs)
        toc = time.time()
        self._timer[func.__name__] += toc - tic
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

            Timer(
            [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
            [{func_name}] cumulative runtime : {hours}h {minutes}m {seconds}s
            -----------
            total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
            )
        """
        string = "Timer(\n"
        for func_name in self._timer.keys():
            # Conversion in hours, minutes, seconds.
            hours, remainder = divmod(self._timer[func_name], 3600)
            minutes, seconds = divmod(remainder, 60)
            string += f"[{func_name}] cumulative runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
        # Adding total runtime.
        hours, remainder = divmod(self.total_runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        string += f"-----------\ntotal runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n)"
        return string