import pytest
import sys
import os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.cross_validation import mean_std_cross_val_scores
from sklearn.linear_model import LogisticRegression

# Small synthetic dataset
X_train_small = pd.DataFrame({
    "feature1": [1, 2, 3, 4],
    "feature2": [5, 6, 7, 8]
})
y_train_small = pd.Series([0, 1, 0, 1])


# Test 1: Check output format - Output should be a pandas Series
def test_mean_std_cross_val_scores_output_format():
    model = LogisticRegression()
    result = mean_std_cross_val_scores(model, X_train_small, y_train_small, cv=2)
    assert isinstance(result, pd.Series)


# Test 2: Check output content - Output should contain formatted strings with mean and std
def test_mean_std_cross_val_scores_output_content():
    model = LogisticRegression()
    result = mean_std_cross_val_scores(model, X_train_small, y_train_small, cv=2)
    assert all("+/-" in str(x) for x in result)


# Test 3: Handle mismatched dimensions
def test_mean_std_cross_val_scores_mismatched_dimensions():
    X_train = pd.DataFrame({"feature1": [1, 2, 3, 4]})
    y_train = pd.Series([0, 1, 0])  
    model = LogisticRegression()
    with pytest.raises(ValueError):
        mean_std_cross_val_scores(model, X_train, y_train, cv=2)


# Test 4: Handle empty input
def test_mean_std_cross_val_scores_empty_data():
    X_train = pd.DataFrame()
    y_train = pd.Series(dtype=int)
    model = LogisticRegression()
    with pytest.raises(ValueError):
        mean_std_cross_val_scores(model, X_train, y_train, cv=2)


# Test 5: Handle invalid model
def test_invalid_model():
    invalid_model = "dsci522"
    with pytest.raises(ValueError):
        mean_std_cross_val_scores(invalid_model, X_train_small, y_train_small, cv=2)


# Test 6: Handle custom scoring
def test_custom_scoring():
    from sklearn.metrics import make_scorer, accuracy_score
    X_train = pd.DataFrame({"feature1": [1, 2, 3, 4], "feature2": [5, 6, 7, 8]})
    y_train = pd.Series([0, 1, 0, 1])
    model = LogisticRegression()
    scoring = ["accuracy", "f1"]
    result = mean_std_cross_val_scores(model, X_train_small, y_train_small, cv=2, scoring=scoring)
    assert "test_accuracy" in result.index, "Output should include custom scoring metric"


# Test 7: Handle invalid arguments
def test_invalid_kwargs():
    model = LogisticRegression()
    with pytest.raises(TypeError):
        mean_std_cross_val_scores(model, X_train_small, y_train_small, invalid_arg="test")


