import time 
import datetime
import copy
from typing import List, Tuple
from .decorator import Decorator

class TimerCounterLogger(Decorator):
    """
    Compute the number of call of various functions and the runtime each call. 

    .. warning::
        If 2 functions/methods have the same '__name__' attribute, the TimerCounterLogger will combined the two runtimes. 
    """

    __help__ = """
    # =======================
    # HELP TimerCounterLogger
    # =======================
    
    Create a timer-counter-logger with :  
    >>> timercounterlogger = TimerCounterLogger()
    
    Then decorate functions with the timer-counter-logger. (@timercounterlogger)

    Initialize and clear the timer-counter-logger with : 
    >>> timercounterlogger = initialize()

    Use the functions and the timer-counter-logger will compute calls.

    To deactivate and re-activate the timer-counter-logger, use :
    >>> timercounterlogger.set_activated()
    >>> timercounterlogger.set_deactivated()

    Print the calls with 3 differents representation (default = resume_repr):
    
    >>> print(timercounterlogger.resume_repr)
    >>> print(timercounterlogger)

    The result will be :
    TimerCounterLogger(
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
    -----------
    total number of calls : {total_runcall}
    total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
    )

    >>> print(timercounterlogger.date_repr)

    The result will be :
    TimerCounterLogger(
    [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
    [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
    [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
    [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
    -----------
    total number of calls : {total_runcall}
    total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
    )

    >>> print(timercounterlogger.name_repr)

    The result will be :
    TimerCounterLogger(
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
    [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
            [{date}] runtime : {hours}h {minutes}m {seconds}s
    -----------
    total number of calls : {total_runcall}
    total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
    )

    """


    def __init__(self):
        super().__init__()
        self.initialize()

    @property
    def logger(self) -> List[Tuple[datetime, str, float]]:
        """
        Returns a copy of the copy
        """
        return copy.deepcopy(self._logger)

    @property
    def total_runtime(self) -> float:
        """
        Returns the total runtime in seconds.
        """
        return sum(logcall[2] for logcall in self._logger)

    @property
    def total_runcall(self) -> int:
        """
        Returns the total runcall.
        """
        return len(self._logger)

    def number_calls(self, func_name: str) -> int:
        """
        Computes the name of call of the given function.

        .. warning::
            If 2 functions/methods have the same '__name__' attribute, the TimerCounterLogger will combined the two.

        Parameters
        ----------
            func_name: str 
                The name of the function.

        Returns
        -------
            N_calls: int
                The number of call of the function with the given name.

        Raises
        ------
            TypeError: If the function name is not a string.
        """
        if not isinstance(func_name, str):
            raise TypeError("Parameter func_name is not a string.")
        return sum(1 for logcall in self._logger if logcall[1] == func_name)

    def cumul_runtime(self, func_name: str) -> int:
        """
        Computes the runtime of the given function.

        .. warning::
            If 2 functions/methods have the same '__name__' attribute, the TimerCounterLogger will combined the two.

        Parameters
        ----------
            func_name: str 
                The name of the function.

        Returns
        -------
            runtime: float
                The cumulative runtime of the function with the given name in seconds.

        Raises
        ------
            TypeError: If the function name is not a string.
        """
        if not isinstance(func_name, str):
            raise TypeError("Parameter func_name is not a string.")
        return sum(logcall[2] for logcall in self._logger if logcall[1] == func_name)

    def get_functions(self) -> List[str]:
        """
        Returns the list containing all the logged functions.

        The result is sorted in alphabetic order.

        Returns
        -------
            func_names: float
                The names of the logged functions.
        """
        func_names = list(set(logcall[1] for logcall in self._logger))
        func_names.sort()
        return func_names
    
    def get_logcall(self, func_name: str) -> List[Tuple[datetime.datetime, str, float]]:
        """
        Extract the part of the logger whose function name is the given function name. 

        The result is sorted in date order.

        Parameters
        ----------
            func_name: str 
                The name of the function.

        Returns
        -------
            logcalls: float
                The logcalls of the function with the given name.

        Raises
        ------
            TypeError: If the function name is not a string.
        """
        if not isinstance(func_name, str):
            raise TypeError("Parameter func_name is not a string.")
        logcalls = [logcall for logcall in self._logger if logcall[1] == func_name]
        logcalls.sort(key=lambda logcall: logcall[0])
        return logcalls

    def sort_by_date(self) -> None:
        """
        Sorts the logger list by date.
        """
        self._logger.sort(key=lambda logcall: logcall[0])
    
    def sort_by_name(self) -> None:
        """
        Sorts the logger list by function name.
        """
        self._logger.sort(key=lambda logcall: logcall[1])

    def initialize(self) -> None:
        """
        Initializes the logger.
        """
        self._logger = [] # (date, function name, runtime)

    def __repr__(self) -> str:
        """
        Returns the string representation.
        """
        return self.resume_repr

    def _wrapper(self, func, *args, **kwargs):
        """
        Runs the function with runtime measurement.
        """
        # Runtime measurement.
        date = datetime.datetime.now()
        tic = time.time()
        outputs = func(*args, **kwargs)
        toc = time.time()
        self._logger.append([date, func.__name__, toc - tic])
        # Return outputs of func.
        return outputs

    #### REPRESENTATION 

    @property
    def date_repr(self) -> str:
        """
        Returns the string representation in the following format:

        TimerCounterLogger(
        [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
        [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
        [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
        [{date}] function : {func_name} - runtime : {hours}h {minutes}m {seconds}s
        -----------
        total number of calls : {total_runcall}
        total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
        )
        """
        string = "TimerCounterLogger(\n"
        self.sort_by_date()
        for logcall in self._logger:
            # Conversion in hours, minutes, seconds.
            hours, remainder = divmod(logcall[2], 3600)
            minutes, seconds = divmod(remainder, 60)
            string += f"[{logcall[0]}] function : {logcall[1]} - runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
        # Adding total runtime and total call number.
        hours, remainder = divmod(self.total_runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        string += f"-----------\ntotal number of calls : {self.total_runcall}\ntotal runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n)"
        return string
    
    def _name_representation(self, develop: bool = True) -> str:
        """
        Returns the string representation in the following format:

        TimerCounterLogger(
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
        [{func_name}] number of calls : {Ncalls} - cumulative runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
                [{date}] runtime : {hours}h {minutes}m {seconds}s
        -----------
        total number of calls : {total_runcall}
        total runtime : {total_runtime_hours}h {total_runtime_minutes}m {total_runtime_seconds}s
        )

        Parameters
        ----------
            develop: bool, optional
                If True the [date] are send, else only major informations.
                Default is True.

        Raises
        ------
            TypeError : if develop is not a booleen.
        """
        if not isinstance(develop, bool):
            raise TypeError("Parameter develop is not a booleen.")
        string = "TimerCounterLogger(\n"
        func_names = self.get_functions()
        for func_name in func_names:
            # Conversion in hours, minutes, seconds.
            Ncalls = self.number_calls(func_name)
            cumul_runtime = self.cumul_runtime(func_name)
            hours, remainder = divmod(cumul_runtime, 3600)
            minutes, seconds = divmod(remainder, 60)
            string += f"[{func_name}] number of calls : {Ncalls} - cumulative runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
            if develop:
                logcalls = self.get_logcall(func_name)
                # Writting the call of the given function.
                for logcall in logcalls:
                    hours, remainder = divmod(logcall[2], 3600)
                    minutes, seconds = divmod(remainder, 60)
                    string += f"\t\t[{logcall[0]}] {Ncalls} runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
        # Adding total runtime and total call number.
        hours, remainder = divmod(self.total_runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        string += f"-----------\ntotal number of calls : {self.total_runcall} calls\ntotal runtime : {int(hours)}h {int(minutes)}m {seconds:.4f}s\n"
        return string

    @property
    def name_repr(self) -> str:
        return self._name_representation(develop=True)
    
    @property
    def resume_repr(self) -> str:
        return self._name_representation(develop=False)