import collections
from importlib.machinery import BuiltinImporter, FrozenImporter
from types import ModuleType
from typing import Any, Callable, Hashable, Optional
from .utils.module import get_module_imports, is_user_defined_module
from . import setup_recording

ignored_object_methods = {
    '__class__',
    '__dir__',
    '__getattribute__',
    '__init__',
    '__new__',
    '__delattr__',
    '__doc__',
    '__getnewargs__',
    '__init_subclass__',
    '__reduce__',
    '__reduce_ex__',
    '__sizeof__',
    '__subclasshook__',
    '__delitem__',
    '__alloc__',
    '__setformat__',
    '__format__',  # Can be removed after fix in restrict.
}

comparison_operations = {'__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__ne__'}

ignored_r_methods = {
    '__radd__',
    '__rand__',
    '__rdivmod__',
    '__rfloordiv__',
    '__rlshift__',
    '__rmod__',
    '__rmul__',
    '__ror__',
    '__rpow__',
    '__rrshift__',
    '__rsub__',
    '__rtruediv__',
    '__rxor__',
}

ignored_methods = set.union(
    ignored_object_methods, comparison_operations, ignored_r_methods
)

ignored_specifics = {
    (dict, '__iter__'),
}

ignored_classes = {BuiltinImporter, FrozenImporter}


def is_ignored(class_: Optional[type], method_name: Optional[str]) -> bool:
    return (
        (
            class_
            and (
                class_ in ignored_classes
                or not issubclass(class_, Hashable)
                and method_name == '__hash__'
            )
        )
        or method_name in ignored_methods
        or (class_, method_name) in ignored_specifics
    )


def get_def_ignored_modules() -> tuple[set[ModuleType], set[Callable[..., Any]]]:
    setup_modules, setup_callables = get_module_imports(setup_recording, set())
    setup_modules = {
        module for module in setup_modules if is_user_defined_module(module)
    }

    return setup_modules, setup_callables
