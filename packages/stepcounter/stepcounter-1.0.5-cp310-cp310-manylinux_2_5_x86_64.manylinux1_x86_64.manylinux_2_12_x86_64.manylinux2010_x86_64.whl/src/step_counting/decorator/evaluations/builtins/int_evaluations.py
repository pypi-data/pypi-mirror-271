from typing import Any, Callable, Literal, Sequence
from ..complexities import (
    ComplexitiesDict,
    constant,
    logarithmic,
    linear,
    linear_to_sec,
    logarithmic_to_sec,
    quadratic,
)


def linear_to_len(args: tuple[Sequence[Any]]) -> int:
    return len(args[0])


# TODO finish
def quadratic_to_bit_len(args: tuple[int]) -> int:
    n = args[0]
    return n.bit_length() ** 2


int_complexities: ComplexitiesDict = {
    '__add__': constant,
    '__lt__': constant,
    '__le__': constant,
    '__eq__': constant,
    '__ne__': constant,
    '__gt__': constant,
    '__ge__': constant,
    '__and__': constant,
    '__floordiv__': constant,
    '__invert__': constant,
    '__lshift__': constant,
    '__mod__': constant,
    '__mul__': constant,
    '__neg__': constant,
    '__or__': constant,
    '__pow__': logarithmic_to_sec,  # Karatsuba algorithm may be used on large numbers
    '__rshift__': constant,
    '__sub__': constant,
    '__truediv__': constant,
    '__xor__': constant,
    'bit_length': logarithmic,
    'conjugate': constant,
    'from_bytes': linear_to_len,
    'to_bytes': logarithmic,
}
