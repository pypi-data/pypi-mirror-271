from ..complexities import ComplexitiesDict, constant


re_complexities: ComplexitiesDict = {
    'findall': constant,
    'match': constant,
    'compile': constant,
    'sub': constant,
    'search': constant,
}
