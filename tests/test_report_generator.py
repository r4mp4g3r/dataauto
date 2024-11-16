# tests/test_report_generator.py

import pytest
from dataauto.report_generator import generate_report
import pandas as pd
import os

@pytest.fixture
def sample_df():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Salary': [70000, 80000, 90000],
        'Department': ['Engineering', 'Marketing', 'Sales']
    }
    df = pd.DataFrame(data)
    return df

def test_generate_report(sample_df, tmp_path):
    output_report = tmp_path / "data_report.pdf"
    generate_report(sample_df, output_report=str(output_report))
    assert os.path.exists(output_report)
    # Optionally, you can add more checks to verify the PDF content if needed