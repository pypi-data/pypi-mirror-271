import inspect
import ctypes
from typing import Any, Callable, Optional

from ..patch import py_object as pyo


def is_py_method_def(class_: type, method_name: str) -> bool:
    """
    Determines if methods is part of PyMethodDef.

    Parameters
    ----------
    class_ (type): class
    method_name (str): name of the method

    Returns
    -------
    bool: information if methods is part of PyMethodDef
    """
    return pyo.get_function_mapping(class_, method_name) is None and method_name in dir(
        class_
    )


def get_class_methods(class_: type) -> list[str]:
    """
    Returns a list of class methods.

    Parameters
    ----------
    class_ (type): class

    Returns
    -------
    list: list of names of methods in a class
    """
    members = inspect.getmembers(class_)

    methods = [
        member for member in members if inspect.isroutine(getattr(class_, member[0]))
    ]

    return [method_name for (method_name, _) in methods]


def get_c_method(class_: type, method_name: str) -> Optional[Callable[..., Any]]:
    """
    Returns a method defined in C.

    Parameters
    ----------
    class_ (Optional[type]): class if the method belongs to a class,
    None otherwise
    method_name (str): name of the method

    Returns
    -------
    Optional[Function]: C method if it exists, None otherwise
    """
    tyobj = pyo.PyTypeObject.from_address(id(class_))

    method_mapping_info = pyo.get_function_mapping(class_, method_name)
    if method_mapping_info is None:
        return None

    tp_name, c_method_name, type_ = method_mapping_info
    tp_as_ptr = getattr(tyobj, tp_name)
    if c_method_name is None:
        c_method = tp_as_ptr
    else:
        tp_as = tp_as_ptr[0]
        c_method = getattr(tp_as, c_method_name)

    py_type = ctypes.PYFUNCTYPE(*type_)
    method = ctypes.cast(c_method, py_type)
    return method
