from ..complexities import ComplexitiesDict, constant, logarithmic_to_min, linear


math_complexities: ComplexitiesDict = {
    'acos': constant,
    'cos': constant,
    'asin': constant,
    'sin': constant,
    'atan': constant,
    'atan2': constant,
    'tan': constant,
    'sqrt': constant,
    'isqrt': constant,
    'degrees': constant,
    'radians': constant,
    'trunc': constant,
    'floor': constant,
    'ceil': constant,
    'isclose': constant,
    'gcd': logarithmic_to_min,
    'lcm': logarithmic_to_min,
    'factorial': linear,
}
