# tests/test_cli.py

import pytest
from click.testing import CliRunner
from dataauto.cli import cli
import os
import pandas as pd

@pytest.fixture
def sample_csv(tmp_path):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'Salary': [70000, 80000, 90000, 100000, 110000],
        'Department': ['Engineering', 'Marketing', 'Sales', 'HR', 'Engineering']
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

def test_load_csv_command(sample_csv):
    runner = CliRunner()
    result = runner.invoke(cli, ['load', str(sample_csv), '--format', 'csv'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data loaded from {sample_csv}." in result.output
    assert "Shape:" in result.output

def test_load_json_command(sample_json):
    runner = CliRunner()
    result = runner.invoke(cli, ['load', str(sample_json), '--format', 'json'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data loaded from {sample_json}." in result.output
    assert "Shape:" in result.output

def test_load_excel_command(sample_excel):
    runner = CliRunner()
    result = runner.invoke(cli, ['load', str(sample_excel), '--format', 'excel', '--sheet', 'Sheet1'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data loaded from {sample_excel}." in result.output
    assert "Shape:" in result.output

def test_save_csv_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "output.csv"
    result = runner.invoke(cli, ['save', str(sample_csv), str(output_file), '--format', 'csv'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data saved successfully to {output_file} in CSV format." in result.output
    assert os.path.exists(output_file)

def test_save_json_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "output.json"
    result = runner.invoke(cli, ['save', str(sample_csv), str(output_file), '--format', 'json'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data saved successfully to {output_file} in JSON format." in result.output
    assert os.path.exists(output_file)

def test_save_excel_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "output.xlsx"
    result = runner.invoke(cli, ['save', str(sample_csv), str(output_file), '--format', 'excel', '--sheet', 'TestSheet'])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Data saved successfully to {output_file} in EXCEL format." in result.output
    assert os.path.exists(output_file)

def test_clean_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "cleaned_data.csv"
    # Introduce missing values for testing
    df = pd.read_csv(sample_csv)
    df.loc[0, 'Age'] = None
    df.to_csv(sample_csv, index=False)
    result = runner.invoke(cli, [
        'clean', str(sample_csv),
        '--strategy', 'mean',
        '--columns', 'Age',
        '--output-file', str(output_file)
    ])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Missing values filled using mean strategy for columns: Age." in result.output
    assert f"Cleaned data saved to {output_file}." in result.output
    assert os.path.exists(output_file)

def test_remove_outlier_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "no_outliers.csv"
    result = runner.invoke(cli, [
        'remove-outlier', str(sample_csv),
        '--column', 'Age',
        '--method', 'IQR',
        '--multiplier', '1.5',
        '--output-file', str(output_file)
    ])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    # Depending on data, check the outlier removal
    assert f"Removed 0 outliers from column 'Age' using IQR method." in result.output
    assert f"Cleaned data saved to {output_file}." in result.output
    assert os.path.exists(output_file)

def test_scale_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_file = tmp_path / "scaled_data.csv"
    result = runner.invoke(cli, [
        'scale', str(sample_csv),
        '--columns', 'Age', '--columns', 'Salary',
        '--method', 'standard',
        '--output-file', str(output_file)
    ])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert f"Columns Age, Salary scaled using standard method." in result.output
    assert f"Scaled data saved to {output_file}." in result.output
    assert os.path.exists(output_file)

def test_plot_histogram_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_dir = tmp_path / "plots"
    result = runner.invoke(cli, [
        'plot', str(sample_csv),
        '--plot-type', 'histogram',
        '--columns', 'Age',
        '--output-dir', str(output_dir),
        '--interactive'
    ])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    # Since the actual plotting functions print their own messages, you can check for the existence of files
    assert os.path.exists(output_dir / "Age_histogram.png")
    assert os.path.exists(output_dir / "Age_histogram.html")

def test_plot_scatter_command(sample_csv, tmp_path):
    runner = CliRunner()
    output_dir = tmp_path / "plots"
    result = runner.invoke(cli, [
        'plot', str(sample_csv),
        '--plot-type', 'scatter',
        '--x', 'Age',
        '--y', 'Salary',
        '--output-dir', str(output_dir),
        '--interactive'
    ])
    if result.exit_code != 0:
        print("CLI Output:", result.output)
    assert result.exit_code == 0
    assert os.path.exists(output_dir / "Age_vs_Salary_scatter.png")
    assert os.path.exists(output_dir / "Age_vs_Salary_scatter.html")