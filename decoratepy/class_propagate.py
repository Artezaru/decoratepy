from .decorator import Decorator
from typing import Optional, List
import types

def class_propagate(decorator: Decorator, names: Optional[List[str]] = None):  
    """
    Applies a given decorator to specific methods of a class. 
    
    Parameters
    ----------
        decorator: Decorator
            An instance of the `Decorator` class to apply to the methods.
        
        names: list of str, optional
            A list of method names to which the decorator should be applied.
            If `None`, the decorator is applied to all methods of the class.
            Default value is `None`.

    Returns
    -------
        class_decorator: function
            A class decorator that applies the given decorator to specified methods.

    Raises
    ------
        TypeError:
            - If `decorator` is not an instance of the `Decorator` class.
            - If `names` is provided and is not a list of strings.
            - If any of the specified method names in `names` does not exist in the class.

    Notes
    -----
    - Only methods that are regular functions (of type `types.FunctionType`) will be targeted.
    - Does not apply the decorator to special methods (e.g., `__init__`, `__str__`) unless explicitly listed in `names`.

    Examples
    --------

    .. code-block:: python

        #Decorating specific methods:
        @class_propagate(my_decorator, names=["method1", "method2"])
        class MyClass:
            def method1(self):
                pass
            
            def method2(self):
                pass
            
            def method3(self):
                pass

        #Decorating all methods:
        @class_propagate(my_decorator)
        class MyClass:
            def method1(self):
                pass
            
            def method2(self):
                pass
    """
    if not isinstance(decorator, Decorator):
        raise TypeError("The parameter `decorator` must be an instance of the `Decorator` class.")
    
    if names is not None:
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            raise TypeError("The `names` parameter must be a list of strings or `None`.")

    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            # Check if the attribute is a regular function and matches the specified names
            if isinstance(attr_value, types.FunctionType) and (names is None or attr_name in names):
                setattr(cls, attr_name, decorator(attr_value))
            elif names is not None and attr_name in names and not isinstance(attr_value, types.FunctionType):
                raise TypeError(f"The attribute `{attr_name}` is not a valid method to decorate.")
        return cls

    return class_decorator
