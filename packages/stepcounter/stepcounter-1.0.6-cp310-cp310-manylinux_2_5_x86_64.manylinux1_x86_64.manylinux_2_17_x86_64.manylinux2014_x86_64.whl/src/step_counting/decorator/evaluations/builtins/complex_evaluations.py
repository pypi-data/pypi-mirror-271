from typing import Any, Callable
from ..complexities import ComplexitiesDict, constant, logarithmic_to_sec

# TODO recheck, mul and pow are quite difficult
complex_complexities: ComplexitiesDict = {
    '__add__': constant,
    '__sub__': constant,
    '__mul__': constant,
    '__pow__': logarithmic_to_sec,
    '__truediv__': constant,
    'conjugate': constant,
    'imag': constant,
    'real': constant,
}
