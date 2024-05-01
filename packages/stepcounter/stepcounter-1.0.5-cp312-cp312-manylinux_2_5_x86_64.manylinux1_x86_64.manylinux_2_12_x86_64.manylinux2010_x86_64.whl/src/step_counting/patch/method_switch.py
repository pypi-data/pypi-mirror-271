from typing import Any, Callable


def is_method(method: Callable[..., Any]) -> bool:
    return callable(method) or type(method) in {classmethod, staticmethod}


class MethodSwitch:
    """
    A class representing a method switch,

    Attributes
    ----------
    overwrite (Function): function which can overwrite the method
    orig_method (Function): original method
    repl_method (Function): replacement method
    """

    def __init__(
        self: 'MethodSwitch',
        overwrite: Callable[..., Any],
        orig_method: Callable[..., Any],
        repl_method: Callable[..., Any],
    ) -> None:
        """
        Initializes a new MethodSwitch instance.

        Returns
        -------
        None
        """
        if not is_method(repl_method):
            raise Exception('Given replacement function is not callable')

        self.overwrite = overwrite
        self.__original_method = orig_method
        self.__replacement_method = repl_method

    def set_original_method(
        self: 'MethodSwitch', orig_method: Callable[..., Any]
    ) -> None:
        """
        Sets original method.
        Parameters
        ----------
        orig_method(Function): original method

        Returns
        -------
        None
        """
        self.__original_method = orig_method

    def set_replacement_method(
        self: 'MethodSwitch', repl_method: Callable[..., Any]
    ) -> None:
        """
        Sets replacement method.

        Parameters
        ----------
        repl_method(Function): replacement method

        Returns
        -------
        None
        """
        if not is_method(repl_method):
            raise Exception('Given replacement function is not callable')
        self.__replacement_method = repl_method

    def get_original_method(self: 'MethodSwitch') -> Callable[..., Any]:
        """
        Returns original method.

        Returns
        -------
        Function: original method
        """
        return self.__original_method

    def get_replacement_method(self: 'MethodSwitch') -> Callable[..., Any]:
        """
        Returns replacement method.

        Returns
        -------
        Function: replacement method
        """
        return self.__replacement_method
