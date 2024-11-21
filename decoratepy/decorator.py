class Decorator(object):
    def __init__(self):
        self._activated = True # The decorator is activated by default.
    
    @property
    def is_activated(self) -> bool:
        """ 
        Returns decorator activation status.
        
        Returns
        -------
            activated: bool
                If the decorator is activated.

        See also
        --------
            - is_deactivated
            - set_activated
        """
        return self._activated

    @property
    def is_deactivated(self) -> bool:
        """ 
        Returns decorator activation status.
        
        Returns
        -------
            desactivated: bool
                If the decorator is deactivated.

        See also
        --------
            - is_activated
            - set_deactivated
        """
        return not self._activated

    def set_activated(self, activated: bool = True) -> None:
        """
        Sets the decorator activation status.
        
        Parameters
        ----------
            activated: bool, optional
                The activation status to apply to the decorator.
                Default value is True
        
        Raises
        ------
            TypeError: If the given argument is not a booleen.

        See also
        --------
            - is_activated
            - set_deactivated
        """
        if not isinstance(activated, bool):
            raise TypeError("Parameter activated is not a booleen.")
        self._activated = activated

    def set_deactivated(self, deactivated: bool = True) -> None:
        """
        Sets the decorator activation status.
        
        Parameters
        ----------
            deactivated: bool, optional
                The negation of the activation status to apply to the decorator.
                Default value is True
        
        Raises
        ------
            TypeError: If the given argument is not a booleen.

        See also
        --------
            - is_deactivated
            - set_activated
        """
        if not isinstance(deactivated, bool):
            raise TypeError("Parameter deactivated is not a booleen.")
        self._activated = not deactivated

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            if self._activated:
                return self.wrapper(func, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapped