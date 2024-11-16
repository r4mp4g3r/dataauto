# tests/test_utils.py

import pytest
from dataauto.utils import validate_file_path, create_output_dir
import os

def test_validate_file_path(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.touch()
    assert validate_file_path(str(file_path)) == True
    non_existent_path = tmp_path / "non_existent.txt"
    assert validate_file_path(str(non_existent_path)) == False

def test_create_output_dir(tmp_path):
    output_dir = tmp_path / "new_dir"
    assert not os.path.exists(str(output_dir))
    create_output_dir(str(output_dir))
    assert os.path.exists(str(output_dir))
    # Cleanup
    os.rmdir(str(output_dir))