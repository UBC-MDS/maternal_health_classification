# fit_classifier.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-05

import pandas as pd
import os
import sys
import numpy as np
import click
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from scipy.stats import loguniform, uniform, randint
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.cross_validation import mean_std_cross_val_scores

@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--best_model_to', type=str, help="Path to directory where the best model object will be written to")
@click.option('--tbl_to', type=str, help="Path to directory where the tables will be written to")
@click.option('--seed', type=int, help="Random seed", default=111)

def main(training_data, best_model_to, tbl_to, seed):
    np.random.seed(seed)
    
    # Read in training data and split into X and y
    train_df = pd.read_csv(training_data)
    X_train = train_df.drop(columns=["RiskLevel"])
    y_train = train_df["RiskLevel"]
    
    # Data Validation for Checking Correlation
    maternal_train_ds = Dataset(train_df, label="RiskLevel", cat_features=[])
    check_feat_corr = FeatureFeatureCorrelation()
    check_feat_corr_result = check_feat_corr.run(maternal_train_ds)
    
    # DummyClassifier, Gaussian Bayes, Decision Tree, Logistic Regression, SVC
    models = {
        "Dummy Classifier": DummyClassifier(random_state=123),
        "Gaussian Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(random_state=123),
        "RBF SVM": SVC(random_state=123),
        "Logistic Regression": LogisticRegression(max_iter=2000, random_state=123),
    }
    
    results_df = None
    results_dict = {}
    for model_name, model in models.items():
        clf_pipe = make_pipeline(StandardScaler(), model)
        results_dict[model_name] = mean_std_cross_val_scores(
            clf_pipe, X_train, y_train, cv=10, return_train_score=True, error_score='raise'
        )
    results_df = pd.DataFrame(results_dict).T
    results_df.to_csv(os.path.join(tbl_to, "summary_cv_scores.csv"), index=True)

    dt = DecisionTreeClassifier(random_state=123)
    
    param_dist = {
        'criterion': ['gini', 'entropy'], 
        'max_depth': randint(3, 20),                
    }
    
    random_search = RandomizedSearchCV(dt, param_dist, n_iter=100, n_jobs=-1, return_train_score = True, random_state=123)
    random_search.fit(X_train, y_train)

    with open(os.path.join(best_model_to, "dt_tuned_fit.pickle"), 'wb') as f:
        pickle.dump(random_search, f)

if __name__ == '__main__':
    main()