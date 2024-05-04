"""
Run llmdocgen on a given directory
"""

import pathlib

from . import enrich


def inline_document_file(file_path: pathlib.Path, save=False, new_file: pathlib.Path = None, **kwargs):
    """
    Create inline documentation for a file
    :param file_path: The path to the file to document
    :param save: Whether to update/save the file with the documentation
    :param new_file: The path to save the documentation to
    :param kwargs: Additional arguments to pass to the completion function
    :return: The completion
    """
    if new_file is None and save:
        new_file = file_path
    completion = enrich.parsed_file_completion(file_path, **kwargs)
    if save:
        new_file.write_text(completion)
    return completion


def run(directory: pathlib.Path, recursive: bool = False, save: bool = False):
    """
    Run llmdocgen on a given directory
    :param directory: The directory to run llmdocgen on
    :param recursive: Whether to run on subdirectories
    :param save: Whether to save the documentation to the file
    """
    for file in directory.iterdir():
        if file.is_dir() and recursive:
            run(file, recursive)
        elif file.is_file():
            completion = inline_document_file(file, save)
            if not save:
                print(completion)


def main():
    """
    Parse command line arguments and run on a given directory.
    """
    import argparse
    parser = argparse.ArgumentParser(description='Run llmdocgen on a given directory')
    parser.add_argument('--recursive', action='store_true', help='Run on subdirectories')
    parser.add_argument('-s', '--save', action='store_true', help='Save the documentation to the file')
    parser.add_argument('directory', type=pathlib.Path, help='The directory to run llmdocgen on')
    args = parser.parse_args()
    run(args.directory, args.recursive, args.save)
