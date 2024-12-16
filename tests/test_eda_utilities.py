import pandas as pd
import numpy as np
import altair as alt
import pytest
import os
import sys
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_utilities import create_heatmap, save_data_summaries

@pytest.fixture
def sample_data():
    """Fixture for creating sample DataFrame."""
    df_eda = pd.DataFrame({
        'Feature1': [1, 2, 3, 4, 5],
        'Feature2': [2, 4, 6, 8, 10],
        'RiskLevel': ['low risk', 'mid risk', 'high risk', 'low risk', 'mid risk']
    })
    return df_eda

@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for creating a temporary directory."""
    return tmp_path

def test_create_heatmap(sample_data, temp_dir):
    df_corr = sample_data.drop(columns=["RiskLevel"])
    plot_to = temp_dir

    # Call the function to create the heatmap
    create_heatmap(df_corr, plot_to)

    # Assert that the file was created
    heatmap_path = os.path.join(plot_to, "heatmap_of_the_maternal_health.png")
    assert os.path.exists(heatmap_path), "Heatmap file was not created."

def test_save_data_summaries(sample_data, temp_dir):
    df_corr = sample_data.drop(columns=["RiskLevel"])
    table_to = temp_dir

    save_data_summaries(sample_data, df_corr, table_to)

    # Assertions: Check if the files are created
    assert os.path.exists(os.path.join(table_to, "df_info.csv"))
    assert os.path.exists(os.path.join(table_to, "df_describe.csv"))
    assert os.path.exists(os.path.join(table_to, "df_shape.csv"))

    # Verify content of the files
    df_info = pd.read_csv(os.path.join(table_to, "df_info.csv"))
    assert list(df_info.columns) == ["Column", "Non-Null Count", "Data Type"]

    df_shape = pd.read_csv(os.path.join(table_to, "df_shape.csv"))
    assert "Rows" in df_shape["Metric"].values
    assert "Columns" in df_shape["Metric"].values
