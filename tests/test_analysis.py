# tests/test_analysis.py
import pytest
import pandas as pd
from dataauto.analysis import load_data, summarize_data, plot_data

def test_load_data():
    df = load_data('examples/sample_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_summarize_data():
    df = load_data('examples/sample_data.csv')
    summary = summarize_data(df)
    assert isinstance(summary, str)
    assert 'count' in summary

def test_plot_data(tmp_path):
    df = load_data('examples/sample_data.csv')
    column = 'Age'  # Adjust based on your sample_data.csv
    plot_data(df, column, save_dir=tmp_path)
    plot_path = tmp_path / f"{column}_distribution.png"
    assert plot_path.exists()