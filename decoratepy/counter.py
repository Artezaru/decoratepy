from .decorator import Decorator

class Counter(Decorator):
    """
    Compute the number of call of various functions. 

    .. warning::
        If 2 functions/methods have the same '__name__' attribute, the Counter will combined the two runcalls. 

    HELP Counter
    ============
    
    Create a counter with :

    .. code-block:: python

        counter = Counter()

    Then decorate functions with the counter. 

    .. code-block:: python

        @counter
        def func_name():
            pass

    Initialize and clear the counter with : 

    .. code-block:: python

        counter = initialize()

    Use the functions and the counter will compute number of calls.

    To deactivate and re-activate the counter, use :

    .. code-block:: python

        counter.set_activated()
        counter.set_deactivated()

    Print the number of calls with :
    
    .. code-block:: python

        print(counter.name_repr) # equivalent of print(counter)

    The result will be :
    
    .. code-block:: console
    
        Counter(
        [{func_name}] number of calls : {Ncalls}
        [{func_name}] number of calls : {Ncalls}
        [{func_name}] number of calls : {Ncalls}
        [{func_name}] number of calls : {Ncalls}
        -----------
        total number of calls : {total_runcall}
        )
    """

    __help__ = """
HELP Counter
============

Create a counter with :

.. code-block:: python

    counter = Counter()

Then decorate functions with the counter. 

.. code-block:: python

    @counter
    def func_name():
        pass

Initialize and clear the counter with : 

.. code-block:: python

    counter = initialize()

Use the functions and the counter will compute number of calls.

To deactivate and re-activate the counter, use :

.. code-block:: python

    counter.set_activated()
    counter.set_deactivated()

Print the number of calls with :

.. code-block:: python

    print(counter.name_repr) # equivalent of print(counter)

The result will be :

.. code-block:: console

    Counter(
    [{func_name}] number of calls : {Ncalls}
    [{func_name}] number of calls : {Ncalls}
    [{func_name}] number of calls : {Ncalls}
    [{func_name}] number of calls : {Ncalls}
    -----------
    total number of calls : {total_runcall}
    )
"""

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
        self._counter = {} # key: str = function name // value: int = number of call

    def __repr__(self) -> str:
        """
        Returns the string representation.
        Default = self.name_repr
        """
        return self.name_repr

    def _wrapper(self, func, *args, **kwargs):
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
        
            Counter(
            [{func_name}] number of calls : {Ncalls}
            [{func_name}] number of calls : {Ncalls}
            [{func_name}] number of calls : {Ncalls}
            [{func_name}] number of calls : {Ncalls}
            -----------
            total number of calls : {total_runcall}
        """
        string = "Counter(\n"
        for func_name in self._counter.keys():
            string += f"[{func_name}] number of calls : {self._counter[func_name]}\n"
        string += f"-----------\ntotal number of calls : {self.total_runcall}\n)"
        return string