from ..complexities import ComplexitiesDict, constant, linear_to_sec


fractions_complexities: ComplexitiesDict = dict()

fractions_fraction_complexities: ComplexitiesDict = {
    'as_integer_ratio': constant,
    'conjugate': constant,
    'denominator': constant,
    'from_decimal': constant,
    'from_float': constant,
    'imag': constant,
    'limit_denominator': linear_to_sec,
    'numerator': constant,
    'real': constant,
}
