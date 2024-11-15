# tests/test_utils.py
from dataauto.utils import validate_file_path

def test_validate_file_path_exists():
    assert validate_file_path('examples/sample_data.csv') == True

def test_validate_file_path_not_exists():
    assert validate_file_path('nonexistent_file.csv') == False