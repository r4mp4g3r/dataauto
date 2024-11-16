# tests/test_data_loader.py

import pytest
from dataauto.data_loader import load_csv, load_json, load_excel, load_sql
import pandas as pd
from unittest.mock import MagicMock

@pytest.fixture
def sample_csv(tmp_path):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Salary': [70000, 80000, 90000],
        'Department': ['Engineering', 'Marketing', 'Sales']
    }
    df = pd.DataFrame(data)
    file = tmp_path / "sample_data.csv"
    df.to_csv(file, index=False)
    return file

@pytest.fixture
def sample_json(tmp_path):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Salary': [70000, 80000, 90000],
        'Department': ['Engineering', 'Marketing', 'Sales']
    }
    df = pd.DataFrame(data)
    file = tmp_path / "sample_data.json"
    df.to_json(file, orient='records', lines=True)
    return file

@pytest.fixture
def sample_excel(tmp_path):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Salary': [70000, 80000, 90000],
        'Department': ['Engineering', 'Marketing', 'Sales']
    }
    df = pd.DataFrame(data)
    file = tmp_path / "sample_data.xlsx"
    df.to_excel(file, index=False)
    return file

def test_load_csv(sample_csv):
    df = load_csv(str(sample_csv))
    assert not df.empty
    assert df.shape == (3, 4)
    assert list(df.columns) == ['Name', 'Age', 'Salary', 'Department']

def test_load_json(sample_json):
    df = load_json(str(sample_json))
    assert not df.empty
    assert df.shape == (3, 4)
    assert list(df.columns) == ['Name', 'Age', 'Salary', 'Department']

def test_load_excel(sample_excel):
    df = load_excel(str(sample_excel))
    assert not df.empty
    assert df.shape == (3, 4)
    assert list(df.columns) == ['Name', 'Age', 'Salary', 'Department']

def test_load_sql_postgresql(mocker):
    # Mock create_engine and the connection
    mock_engine = mocker.patch('dataauto.data_loader.create_engine')
    mock_connection = mocker.Mock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection

    # Mock pd.read_sql_query to return a predefined DataFrame
    sample_data = pd.DataFrame([
        {'Name': 'Alice', 'Age': 25, 'Salary': 70000, 'Department': 'Engineering'},
        {'Name': 'Bob', 'Age': 30, 'Salary': 80000, 'Department': 'Marketing'},
        {'Name': 'Charlie', 'Age': 35, 'Salary': 90000, 'Department': 'Sales'},
    ])
    mocker.patch('dataauto.data_loader.pd.read_sql_query', return_value=sample_data)

    query = "SELECT Name, Age, Salary, Department FROM employees"
    df = load_sql('postgresql', 'localhost', 5432, 'testdb', 'user', 'password', query)
    assert not df.empty
    assert df.shape == (3, 4)
    assert list(df.columns) == ['Name', 'Age', 'Salary', 'Department']

def test_load_sql_mysql(mocker):
    # Mock create_engine and the connection
    mock_engine = mocker.patch('dataauto.data_loader.create_engine')
    mock_connection = mocker.Mock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection

    # Mock pd.read_sql_query to return a predefined DataFrame
    sample_data = pd.DataFrame([
        {'Name': 'Alice', 'Age': 25, 'Salary': 70000, 'Department': 'Engineering'},
        {'Name': 'Bob', 'Age': 30, 'Salary': 80000, 'Department': 'Marketing'},
        {'Name': 'Charlie', 'Age': 35, 'Salary': 90000, 'Department': 'Sales'},
    ])
    mocker.patch('dataauto.data_loader.pd.read_sql_query', return_value=sample_data)

    query = "SELECT Name, Age, Salary, Department FROM employees"
    df = load_sql('mysql', 'localhost', 3306, 'testdb', 'user', 'password', query)
    assert not df.empty
    assert df.shape == (3, 4)
    assert list(df.columns) == ['Name', 'Age', 'Salary', 'Department']