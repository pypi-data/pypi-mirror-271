from ..complexities import ComplexitiesDict, constant


csv_complexities: ComplexitiesDict = {
    'reader': constant,
    'writer': constant,
}

csv_dictreader_complexities: ComplexitiesDict = {
    'fieldnames': constant,
}
