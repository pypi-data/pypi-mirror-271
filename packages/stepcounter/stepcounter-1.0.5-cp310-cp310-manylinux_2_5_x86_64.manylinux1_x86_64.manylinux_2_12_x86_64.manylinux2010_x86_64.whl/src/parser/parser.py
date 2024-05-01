import argparse


def setup_parser() -> argparse.ArgumentParser:
    """
    Sets up argument parser.

    Returns
    -------
    ArgumentParser:  ArgumentParser with added arguments.
    """
    parser = argparse.ArgumentParser(description='Parse command line arguments')
    parser.add_argument('input_file', type=str, help='Input file')
    parser.add_argument('-p', '--profile', type=bool, help='Profile', required=False)
    parser.add_argument(
        '-o', '--output_dir', type=str, help='Output directory', required=False
    )

    return parser
