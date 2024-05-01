import sys
from types import BuiltinFunctionType, FunctionType, MethodType, ModuleType
from typing import Any, Callable, Optional, Union


from ..original_methods import _hash, dict_get

Py_LT, Py_LE, Py_EQ, Py_NE, Py_GT, Py_GE = range(6)
comparison_methods = {
    Py_LT: '__lt__',
    Py_LE: '__le__',
    Py_EQ: '__eq__',
    Py_NE: '__ne__',
    Py_GT: '__gt__',
    Py_GE: '__ge__',
}

########################################################################################
# These method are used with patches aplied. Therefore use of regular methods is
# severly limited.
# To avoid unwanted recursion it is necessary to use methods that have not been
# decorated by this decorator.
########################################################################################


def module_in_list(module: Optional[ModuleType], modules: set[ModuleType]) -> bool:
    """
    !IMPORTANT: This function is used with patches applied. Therefore the
    presence of a module in list can't be determined with:

                    module in list of modules

    This would cause recursion. Therefore this fuction uses hashes instead.

    Checks if module is present in list of modules.

    Parameters
    ----------
    module (ModuleType): Module which defines the class/method
    modules (set): set of modules

    Returns
    -------
    bool: information if the module is present in the list
    """
    for item in set.__iter__(modules):
        if int.__eq__(_hash(module), _hash(item)):
            return True
    return False


def determine_method(method_name: str, args: tuple[Any, ...]) -> str:
    """
    Names of some function is determined by it's argument.
    Determines the name of a method.

    Parameters
    ----------
    method_name (str): collective name of method
    args (tuple): arguments of the method

    Returns
    -------
    str: name of the method

    Example
    -------
    All comparison operations are internally performed by a single method.
    Based on the last argument of this method, we can determine which
    comparison method was originally called.
    """
    if str.__eq__(method_name, 'comparison'):
        return dict.__getitem__(comparison_methods, tuple.__getitem__(args, 2))

    return method_name


def get_caller_module_info() -> tuple[Optional[ModuleType], int]:
    """
    Returns module and line from which the function was called.

    Returns
    -------
    ModuleType: module if the caller moduel can be found, None otherwise
    int: no of line from which the method was called
    """
    try:
        caller_frame = sys._getframe(2)
    except:
        return None, 0

    module_name = dict_get(caller_frame.f_globals, '__name__', None)
    line_number = caller_frame.f_lineno

    module = dict_get(sys.modules, module_name, None)

    return module, line_number


########################################################################################


def get_method_type(
    orig_module: ModuleType, class_: Optional[type], method_name: str
) -> Callable[..., Any]:
    """
    Returns type of a method based on combination of module, class and name.

    Parameters
    ----------
    module (ModuleType): Module which defines the class/method
    class_ (Optional[type]): class which defines the method, None if the
    function is not defined by class
    funct_name (str): name of the function

    Returns
    -------
    Function: type of a method
    """
    if method_name == 'comparison':
        return FunctionType

    parent = orig_module if class_ is None else class_
    if hasattr(parent, '__dict__') and method_name in parent.__dict__:
        method = parent.__dict__[method_name]
        if isinstance(method, staticmethod):
            return staticmethod
        elif isinstance(method, classmethod):
            return classmethod

    method = getattr(parent, method_name, None)
    if method:
        if isinstance(method, (BuiltinFunctionType, MethodType)):
            return staticmethod
        elif callable(method):
            return FunctionType

    if method_name == '__hash__':
        return staticmethod
    raise ValueError(f'Method {method_name} not found in {parent}.')
