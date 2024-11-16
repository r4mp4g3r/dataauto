# tests/test_model_trainer.py

import pytest
import pandas as pd
from dataauto.model_trainer import train_model
import joblib
import os
import warnings
from sklearn.exceptions import UndefinedMetricWarning

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

def test_train_regressor(sample_csv, tmp_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        output_model = tmp_path / "trained_model.joblib"
        output_report = tmp_path / "model_report.txt"
        df = pd.read_csv(sample_csv)
        model, report = train_model(df, target='Salary', model_type='regressor', test_size=0.2, random_state=42)
        # Save the model and report
        joblib.dump(model, str(output_model))
        with open(str(output_report), 'w') as f:
            f.write(report)
        # Assertions
        assert model is not None
        assert "Mean Squared Error" in report
        assert "R^2 Score" in report
        assert os.path.exists(output_model)
        assert os.path.exists(output_report)

def test_train_classifier(sample_csv, tmp_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        output_model = tmp_path / "trained_classifier.joblib"
        output_report = tmp_path / "model_classifier_report.txt"
        df = pd.read_csv(sample_csv)
        model, report = train_model(df, target='Department', model_type='classifier', test_size=0.2, random_state=42)
        # Save the model and report
        joblib.dump(model, str(output_model))
        with open(str(output_report), 'w') as f:
            f.write(report)
        # Assertions
        assert model is not None
        assert "precision" in report.lower()
        assert "recall" in report.lower()
        assert os.path.exists(output_model)
        assert os.path.exists(output_report)