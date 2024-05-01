from typing import Any

from ..complexities import (
    ComplexitiesDict,
    constant,
    linear_to_len,
    comparison_com,
    linearithmic_to_len,
    comparison_com,
)


def list_del_complexity(args: tuple[list[Any], int]) -> int:
    list_ = args[0]
    index = args[1]
    return len(list_) - index


def list_extend_complexity(args: tuple[list[Any], list[Any]]) -> int:
    extending_list = args[1]

    return len(extending_list)


def list_insert_complexity(args: tuple[list[Any], int]) -> int:
    list_ = args[0]
    index = args[1]
    return len(list_) - index + 1


def list_mul_complexity(args: tuple[list[Any], int]) -> int:
    list_ = args[0]
    multiplier = args[1]
    return multiplier * len(list_)


def list_pop_complexity(args: tuple[list[Any], int]) -> int:
    # In this case, pop is used without a second argument
    # therefore we are popping from the end of the list
    # making the time complexity constant.
    if len(args) < 2:
        return 1

    list_ = args[0]
    index = args[1]
    return len(list_) - index


def list_slice_complexity(args: tuple[list[Any], int]) -> int:
    list_ = args[0]
    multiplier = args[1]
    return multiplier * len(list_)


list_complexities: ComplexitiesDict = {
    'append': constant,
    'clear': constant,
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    'comparison': linear_to_len,
    '__contains__': linear_to_len,
    'copy': linear_to_len,
    'count': linear_to_len,
    'del': list_del_complexity,
    'extend': list_extend_complexity,
    '__getitem__': constant,
    'insert': list_insert_complexity,
    '__iter__': linear_to_len,
    '__len__': constant,
    '__mul__': list_mul_complexity,
    'min': linear_to_len,
    'max': linear_to_len,
    'pop': list_pop_complexity,
    'remove': linear_to_len,
    'reverse': linear_to_len,
    'slice': list_slice_complexity,
    'sort': linearithmic_to_len,
    'setitem': constant,
}
