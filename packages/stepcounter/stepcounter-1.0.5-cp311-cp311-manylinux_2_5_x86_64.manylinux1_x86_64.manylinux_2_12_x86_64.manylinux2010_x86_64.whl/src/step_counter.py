from types import ModuleType

from step_counting.setup_recording import setup_recording, RecodingActivated
from profiler.profiler import create_profile, output_profile
from parser.parser import setup_parser
from utils import import_from_path, insert_module_to_path


def main() -> None:
    """
    Main function of the script.

    Script flow:
        - Parse arguments
        - Insert input file to path
        - Import module from input path
        - Setup recording
        - Evaluate function of imported module
        - [OPTIONAL] Profile module
        - print overall score

    Returns
    -------
    None
    """
    parser = setup_parser()
    args = parser.parse_args()

    input_file = args.input_file
    profile = args.profile
    output_file = args.output_dir

    insert_module_to_path(input_file)

    eval_module: ModuleType = import_from_path(input_file)
    recorder, tracked_modules = setup_recording(eval_module, {'ib111'})

    with RecodingActivated():
        eval_module.main()

    module_profiles = create_profile(tracked_modules, recorder.get_data())

    if profile:
        output_profile(module_profiles, output_file)

    evaluation = recorder.evaluate_data()
    print('SCORE:', evaluation)


if __name__ == '__main__':
    main()
