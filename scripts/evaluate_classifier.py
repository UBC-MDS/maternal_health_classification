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
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

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

    # NEED TO LOAD IN THE BEST MODEL
    with open(best_model_from, 'rb') as f:
        random_search = pickle.load(f)
    
    # Scoring with the best model
    test_score = {'test_score': [random_search.score(X_test, y_test)]}
    test_score = pd.DataFrame(test_score)
    test_score.to_csv(os.path.join(tbl_to, "test_score.csv"), index=False)

    # Decision Tree plot 
    plt.figure(figsize=(15, 5))
    plot_tree(
        random_search.best_estimator_,
        feature_names=X_test.columns,
        class_names=y_test.unique(),
        filled=True,
        max_depth=3  # Adjust the depth for better readability
    )
    plt.savefig(os.path.join(plot_to, "decision_tree.png"))

    confmat_dt = ConfusionMatrixDisplay.from_predictions(
        y_test,
        random_search.predict(X_test),
        display_labels=random_search.best_estimator_.classes_
    )
    plt.title('Confusion Matrix for Decision Tree')
    plt.savefig(os.path.join(plot_to, "confusion_matrix.png"))

    cm = confusion_matrix(y_test, random_search.predict(X_test))
    pd.DataFrame(cm).to_csv(os.path.join(tbl_to, "confusion_matrix.csv"), index=False)
    

if __name__ == '__main__':
    main()