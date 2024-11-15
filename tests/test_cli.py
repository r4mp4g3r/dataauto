# tests/test_cli.py
import pytest
from click.testing import CliRunner
from dataauto.cli import cli

def test_load_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['load', 'examples/sample_data.csv'])
    assert result.exit_code == 0
    assert 'Data loaded from examples/sample_data.csv' in result.output

def test_summarize_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['summarize', 'examples/sample_data.csv'])
    assert result.exit_code == 0
    assert 'count' in result.output  # Assuming the CSV has numerical data

def test_plot_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['plot', 'examples/sample_data.csv', '--column', 'Age'])
    assert result.exit_code == 0
    assert 'Plot saved for column: Age' in result.output

def test_scatter_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['scatter', 'examples/sample_data.csv', '--column_x', 'Age', '--column_y', 'Salary'])
    assert result.exit_code == 0
    assert 'Scatter plot saved as Age_vs_Salary_scatter.png' in result.output