from types import ModuleType
import os
import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec


def import_from_path(file_path: str) -> ModuleType:
    """
    Imports a module from given path.

    Parameters
    ----------
    file_path (str): path to a file with module definition

    Returns
    -------
    ModuleType: module defined on given path
    """
    path = Path(file_path).resolve()
    module_name = path.stem

    spec = spec_from_file_location(module_name, str(path))
    if spec and spec.loader:
        module = module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f'Could not load module from path: {file_path}')


def insert_module_to_path(input_file: str) -> None:
    """
    Inserts module of the input file to path.

    Parameters
    ----------
    input_file (str): path to the input file

    Returns
    -------
    None
    """
    module_dir = os.path.dirname(input_file)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
