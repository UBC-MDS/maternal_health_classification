# eda.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-15

import click
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_utilities import create_heatmap, create_countplot, create_boxplots, save_data_summaries

@click.command()
@click.option('--processed-training-data', type=str, help="Path to processed training data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--table-to', type=str, help="Path to directory where the table will be written to")
def main(processed_training_data, plot_to, table_to):
    '''
    Main function to perform EDA (Exploratory Data Analysis) on the provided dataset.
    '''
    df_eda = pd.read_csv(processed_training_data)

    df_corr = df_eda.copy()
    RiskLevel = {'low risk': 0, 'mid risk': 1, 'high risk': 2}
    df_corr['RiskLevel'] = df_corr['RiskLevel'].map(RiskLevel).astype(float)

    create_heatmap(df_corr, plot_to)
    create_countplot(df_eda, plot_to)
    create_boxplots(df_eda, plot_to)

    save_data_summaries(df_eda, df_corr, table_to)


if __name__ == '__main__':
    main()
