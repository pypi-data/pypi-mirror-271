from typing import Any
from ..complexities import (
    ComplexitiesDict,
    constant,
    linear_to_len,
    comparison_com,
)


def dict_update_complexity(args: tuple[dict[Any, Any], dict[Any, Any]]) -> int:
    dict_one = args[0]
    dict_two = args[1]
    return len(dict_one) + len(dict_two)


# TODO possible problems due to hash collisions...
dict_complexities: ComplexitiesDict = {
    '__contains__': constant,
    '__len__': constant,
    '__getitem__': constant,
    '__iter__': linear_to_len,
    '__setitem__': constant,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    'clear': linear_to_len,
    'copy': linear_to_len,
    'fromkeys': linear_to_len,
    'get': constant,
    'items': linear_to_len,
    'keys': linear_to_len,
    'pop': constant,
    'popitem': constant,
    'setdefault': constant,
    'update': dict_update_complexity,
    'values': linear_to_len,
}
