# dataauto/utils.py

import os

def validate_file_path(file_path):
    """
    Validate if the file path exists and is a file.

    Parameters:
        file_path (str): Path to validate.

    Returns:
        bool: True if valid, else False.
    """
    return os.path.isfile(file_path)

def create_output_dir(output_dir):
    """
    Create the output directory if it doesn't exist.

    Parameters:
        output_dir (str): Directory path to create.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)