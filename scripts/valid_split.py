# download_data.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-4

import click
import pandas as pd
import pandera as pa
import numpy as np
import os
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

@click.command()
@click.option('--raw-data', type=str, help="The path to raw data")
@click.option('--data-dest', type=str, help="The destination path where the data will be saved")
@click.option('--seed', type=int, help="Random seed", default=111)

def main(raw_data, data_dest, seed):
    """This script validates the data, splits the data into a train and test set, and lastly processes the data with Standard Scaler. 
    It saves the split data (a train and test set), and the standard scaler processor object."""
    np.random.seed(seed)
    
    # Read in data
    df = pd.read_csv(raw_data)
    
    #Drop two rows with out of range data
    df = df[df['HeartRate'] != 7]

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
    
    # Split data into train and test sets and save
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=seed)

    train_df.to_csv(os.path.join(data_dest, "train_df.csv"), index=False)
    test_df.to_csv(os.path.join(data_dest, "test_df.csv"), index=False)

    # Data Validation for Checking Correlation
    maternal_train_ds = Dataset(train_df, label="RiskLevel", cat_features=[])

    check_feat_corr = FeatureFeatureCorrelation()
    check_feat_corr_result = check_feat_corr.run(maternal_train_ds)
    check_feat_corr_result

    # Scaled train and test data with Standard Scaler, and save
    numeric_features =  train_df.columns[:-1].to_list()
    passthrough = ['RiskLevel']
    preprocessor = make_column_transformer((StandardScaler(), numeric_features),
                                         ("passthrough", passthrough))
    
    preprocessor.fit(train_df)
    scaled_train_df = pd.DataFrame(preprocessor.transform(train_df))
    scaled_test_df = pd.DataFrame(preprocessor.transform(test_df))

    scaled_train_df.to_csv(os.path.join(data_dest, "scaled_train_df.csv"), index=False)
    scaled_test_df.to_csv(os.path.join(data_dest, "scaled_test_df.csv"), index=False)

if __name__ == '__main__':
    main() 

