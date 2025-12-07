import pandas as pd
import os
import pytest

# Smoke Test: Does the data exist?
def test_data_exists():
    assert os.path.exists("data/CIDDS-001-external-week1.csv"), "Data file not found!"

# Data Integrity Test: Are columns correct?
def test_columns_exist():
    df = pd.read_csv("data/CIDDS-001-external-week1.csv")
    expected_cols = ["Duration", "Packets", "Bytes", "Proto", "Flags", "class"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"

# Quality Test: Is the dataset empty?
def test_not_empty():
    df = pd.read_csv("data/CIDDS-001-external-week1.csv")
    assert len(df) > 0, "Dataset is empty!"