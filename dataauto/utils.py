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