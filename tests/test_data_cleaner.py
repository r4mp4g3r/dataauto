# tests/test_data_cleaner.py

import pytest
from dataauto.data_cleaner import clean_data, remove_outliers
import pandas as pd

@pytest.fixture
def sample_df():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'Salary': [70000, 80000, 90000, 100000, 110000],
        'Department': ['Engineering', 'Marketing', 'Sales', 'HR', 'Engineering']
    }
    df = pd.DataFrame(data)
    return df

def test_clean_data(sample_df):
    # Introduce missing values
    df = sample_df.copy()
    df.loc[0, 'Age'] = None
    df.loc[2, 'Salary'] = None

    cleaned_df = clean_data(df, strategy='mean', columns=['Age', 'Salary'])
    # Assertions
    assert not cleaned_df['Age'].isnull().any()
    assert not cleaned_df['Salary'].isnull().any()
    # Check if the filled values are correct
    expected_age_mean = (30 + 35 + 40 + 45) / 4
    expected_salary_mean = (80000 + 70000 + 100000 + 110000) / 4
    assert cleaned_df.loc[0, 'Age'] == expected_age_mean
    assert cleaned_df.loc[2, 'Salary'] == expected_salary_mean

def test_remove_outliers(sample_df):
    # Introduce outliers
    df = sample_df.copy()
    df.loc[0, 'Age'] = 100  # Outlier
    df_cleaned, removed = remove_outliers(df, column='Age', method='IQR', multiplier=1.5)
    # Assertions
    assert removed == 1
    assert 100 not in df_cleaned['Age'].values
    assert df_cleaned.shape[0] == 4