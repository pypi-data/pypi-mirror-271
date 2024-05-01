from ..complexities import ComplexitiesDict, constant, linear_to_len, comparison_com


tuple_complexities: ComplexitiesDict = {
    '__len__': constant,
    '__getitem__': constant,
    '__contains__': linear_to_len,
    '__iter__': constant,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    'count': linear_to_len,
    'index': linear_to_len,
}
