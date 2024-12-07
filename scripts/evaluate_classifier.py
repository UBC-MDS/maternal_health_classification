# evaluate_classifier.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-05

import click
import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

@click.command()
@click.option('--test_data', type=str, help="Path to test data")
@click.option('--best_model_from', type=str, help="Path to directory where the fit best model object lives")
@click.option('--plot_to', type=str, help="Path to directory where the plot will be written to")
@click.option('--tbl_to', type=str, help="Path to directory where the tables will be written to")
@click.option('--seed', type=int, help="Random seed", default=111)


def main(test_data, best_model_from, plot_to, tbl_to, seed):
    np.random.seed(seed)
    
    # Reading the test data
    test_df = pd.read_csv(test_data)
    X_test = test_df.drop(columns=["RiskLevel"])
    y_test = test_df["RiskLevel"]

    X_test.to_csv(os.path.join(tbl_to, "X_test.csv"), index=True)
    y_test.to_csv(os.path.join(tbl_to, "y_test.csv"), index=True)
    
    # NEED TO LOAD IN THE BEST MODEL
    with open(best_model_from, 'rb') as f:
        random_search = pickle.load(f)
    
    # Scoring with the best model
    random_search.score(X_test, y_test)

    # Decision Tree plot <- NEED TO SAVE !!!!!!!!!!!!
    plt.figure(figsize=(15, 5))
    plot_tree(
        random_search.best_estimator_,
        feature_names=X_test.columns,
        class_names=y_test.unique(),
        filled=True,
        max_depth=3  # Adjust the depth for better readability
    )
    plt.savefig(os.path.join(plot_to, "decision_tree.png"))
    

if __name__ == '__main__':
    main()