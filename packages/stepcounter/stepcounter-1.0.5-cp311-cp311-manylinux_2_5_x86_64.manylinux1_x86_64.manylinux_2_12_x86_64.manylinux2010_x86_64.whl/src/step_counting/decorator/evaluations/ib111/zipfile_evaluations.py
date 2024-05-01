from typing import Any, Callable, Dict
from ..complexities import ComplexitiesDict, constant


zipfile_complexities: ComplexitiesDict = {
    'is_zipfile': constant,
}

zipfile_zipfile_complexities: ComplexitiesDict = {
    'close': constant,
    'comment': constant,
    'extract': constant,
    'extractall': constant,
    'fp': constant,
    'getinfo': constant,
    'infolist': constant,
    'namelist': constant,
    'open': constant,
    'printdir': constant,
    'read': constant,
    'setpassword': constant,
    'testzip': constant,
    'write': constant,
    'writestr': constant,
}
