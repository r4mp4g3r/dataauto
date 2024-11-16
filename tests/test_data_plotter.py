# tests/test_data_plotter.py

import pytest
import pandas as pd
from dataauto.data_plotter import plot_histogram, plot_scatter, plot_box, plot_heatmap, plot_line
import os

@pytest.fixture
def sample_df(tmp_path):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'Salary': [70000, 80000, 90000, 100000, 110000],
        'Department': ['Engineering', 'Marketing', 'Sales', 'HR', 'Engineering']
    }
    df = pd.DataFrame(data)
    return df

def test_plot_histogram(sample_df, tmp_path, capsys):
    output_dir = tmp_path / "plots"
    plot_histogram(sample_df, 'Age', output_dir=str(output_dir), interactive=False)
    captured = capsys.readouterr()
    assert f"Histogram for Age saved to {output_dir}/Age_histogram.png." in captured.out
    assert os.path.exists(output_dir / "Age_histogram.png")

def test_plot_scatter(sample_df, tmp_path, capsys):
    output_dir = tmp_path / "plots"
    plot_scatter(sample_df, 'Age', 'Salary', output_dir=str(output_dir), interactive=False)
    captured = capsys.readouterr()
    assert f"Scatter plot for Age vs Salary saved to {output_dir}/Age_vs_Salary_scatter.png." in captured.out
    assert os.path.exists(output_dir / "Age_vs_Salary_scatter.png")

def test_plot_box(sample_df, tmp_path, capsys):
    output_dir = tmp_path / "plots"
    plot_box(sample_df, 'Age', output_dir=str(output_dir), interactive=False)
    captured = capsys.readouterr()
    assert f"Box plot for Age saved to {output_dir}/Age_boxplot.png." in captured.out
    assert os.path.exists(output_dir / "Age_boxplot.png")

def test_plot_heatmap(sample_df, tmp_path, capsys):
    output_dir = tmp_path / "plots"
    plot_heatmap(sample_df, ['Age', 'Salary'], output_dir=str(output_dir), interactive=False)
    captured = capsys.readouterr()
    assert f"Correlation heatmap saved to {output_dir}/correlation_heatmap.png." in captured.out
    assert os.path.exists(output_dir / "correlation_heatmap.png")

def test_plot_line(sample_df, tmp_path, capsys):
    output_dir = tmp_path / "plots"
    plot_line(sample_df, 'Age', 'Salary', output_dir=str(output_dir), interactive=False)
    captured = capsys.readouterr()
    assert f"Line plot for Salary over Age saved to {output_dir}/Salary_over_Age_line.png." in captured.out
    assert os.path.exists(output_dir / "Salary_over_Age_line.png")