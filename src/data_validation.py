# data_validation.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-13

import pandas as pd
import pandera as pa
import numpy as np
import os
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

def data_validation(df):
    """
    Validates maternal health risk data

    Parameters
    -----------
    raw_data : 
        the dataframe with maternal health risk data

    Returns 
    -----------
    This function does not return anything, it validates the maternal health dataset.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame, got {type(df)}")
    if df.shape[0] == 0:
        raise ValueError("Cannot validate empty an dataframe.")

    # validate data
    schema = pa.DataFrameSchema(
        {
            "RiskLevel": pa.Column(str, pa.Check.isin(["high risk", "mid risk", "low risk"])),
            "Age": pa.Column(int, pa.Check.between(10, 70)),
            "SystolicBP": pa.Column(int, pa.Check.between(65, 185)),
            "DiastolicBP": pa.Column(int, pa.Check.between(40, 125)),
            "BS": pa.Column(float, pa.Check.between(3, 20)),
            "BodyTemp": pa.Column(float, pa.Check.between(94, 105)),
            "HeartRate": pa.Column(int, pa.Check.between(50, 110))
        },
        checks=[
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows present.")
        ]
    )

    # Run validation tests on our dataframe
    schema.validate(df, lazy=True)
    
