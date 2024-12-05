# split_n_preprocess.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-05

import click
import os
import numpy as np
import pandas as pd
import pandera as pa
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector


@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(raw_data, data_to, preprocessor_to, seed):
    '''This script splits the raw data into train and test sets, 
    and then preprocesses the data to be used in exploratory data analysis.
    It also saves the preprocessor to be used in the model training script.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    df = pd.read_csv(raw_data)
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
        #pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows present."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows present.")]
    )
    
    schema.validate(df, lazy=True)
    # create the split
    train_df, test_df =train_test_split(df, test_size=0.2, random_state=123)

    train_df.to_csv(os.path.join(data_to, "maternal_risk_train.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "maternal_risk_test.csv"), index=False)

    maternal_preprocessor = make_column_transformer(
        (StandardScaler(), make_column_selector(dtype_include='number')),
        verbose_feature_names_out=False
    )
    pickle.dump(maternal_preprocessor, open(os.path.join(preprocessor_to, "_preprocessor.pickle"), "wb"))

    maternal_preprocessor.fit(train_df)
    scaled_maternal_risk_train = maternal_preprocessor.transform(train_df)
    scaled_maternal_risk_test = maternal_preprocessor.transform(test_df)

    scaled_maternal_risk_train.to_csv(os.path.join(data_to, "scaled_maternal_risk_train.csv"), index=False)
    scaled_maternal_risk_test.to_csv(os.path.join(data_to, "scaled_maternal_risk_test.csv"), index=False)

if __name__ == '__main__':
    main()