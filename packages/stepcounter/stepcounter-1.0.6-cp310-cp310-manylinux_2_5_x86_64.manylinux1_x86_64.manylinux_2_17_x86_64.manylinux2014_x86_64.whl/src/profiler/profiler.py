import os
from types import ModuleType
from typing import Any, Optional

from step_counting.decorator.records.record_classes import Counter


def create_module_profile(
    module_file: str, module_data: dict[int, dict[Any, Counter]]
) -> str:
    """
    Creates a profile for given module. Information about operations on each
    line are added as commentary at the end of the line.

    Parameters
    ----------
    module_file (str): path to the file where the module is defined
    module_data (dict): data collected for given module

    Returns
    -------
    str: Profile of the program
    """
    lines = []
    with open(module_file, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            lines.append(f'{line_number}: {line[0:-1]}')

            lines.append((90 - len(str(line_number)) - len(line)) * ' ')
            for record, counter in module_data.get(line_number, {}).items():
                module, class_, func = record
                class_name = class_.__name__ + '.' if class_ else ''
                lines.append(
                    f' # {module.__name__}.{class_name}{func}: No of calls: {counter.get_count_total()}, Total eval: {counter.get_evaluation_total()}\n'
                )

                lines.append(91 * ' ')

            lines[-1] = '\n'

    return ''.join(lines)


def create_profile(
    modules: set[ModuleType],
    data: dict[
        ModuleType, dict[int, dict[tuple[ModuleType, Optional[type], str], Counter]]
    ],
) -> dict[ModuleType, str]:
    """
    Creates a profile for all modules.

    Parameters
    ----------
    modules (set): set of modules to profile
    data (dict): data collected for all modules

    Returns
    -------
    dict: returns dictionary with modules as keys and their respective
    profiles
    """
    profiled_modules = dict()
    for module in modules:
        module_data = data.get(module, {})

        assert module.__file__
        profiled_modules[module] = create_module_profile(module.__file__, module_data)

    return profiled_modules


def output_to_stdout(module_profiles: dict[ModuleType, str]) -> None:
    """
    Outputs all given module profiles to stdout

    Parameters
    ----------
    module_profiles (dict): profiles for each module

    Returns
    -------
    None
    """
    for module, profile in module_profiles.items():
        print(module.__name__)
        print(profile)


def profile_to_file(profile: str, output_file: str) -> None:
    """
    Outputs profile to file.

    Parameters
    ----------
    profile (str): profile of a module
    output_file (str): output file to which the profile will be written

    Returns
    -------
    None
    """
    with open(output_file, 'w') as file:
        file.write(profile)


def output_to_dir(module_profiles: dict[ModuleType, str], output_dir: str) -> None:
    """
    Outputs all profiles to directory, each to separate file.

    Parameters
    ----------
    module_profiles (dict): profiles for each module
    output_dit (str): path to the dir to which profile files will be writen

    Returns
    -------
    None
    """
    for module, profile in module_profiles.items():
        filepath = os.path.join(output_dir, module.__name__) + '.py'
        profile_to_file(profile, filepath)


def output_profile(module_profiles: dict[ModuleType, str], output_dir: str) -> None:
    """
    Determines if profiles should be written to stdout or directory.

    Parameters
    ----------
    module_profiles (dict): profiles for each module
    output_dit (str): path to the dir to which profile files will be writen

    Returns
    -------
    None
    """
    if output_dir is None:
        output_to_stdout(module_profiles)
    else:
        output_to_dir(module_profiles, output_dir)
