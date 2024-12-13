import pytest
import sys
import os
import pandas as pd
import pandera as pa
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_validation import data_validation

test_data = pd.DataFrame({
    "RiskLevel" : ["high risk", "mid risk", "low risk"],
    "Age": [np.nan, 1, 20],
    "SystolicBP": [10, np.nan, 70],
    "DiastolicBP": [250, np.nan, 100], 
    "BS": [9, np.nan, 50],
    "BodyTemp": [96, np.nan, 125],
    "HeartRate": [15, np.nan, 75]
})

# Test Case: wrong type passed to function
test_data_list = list(
    "RiskLevel" : ["high risk", "mid risk", "low risk"],
    "Age": [35, 15, 20],
    "SystolicBP": [150, 110, 70],
    "DiastolicBP": [80, 65, 100], 
    "BS": [9, 4, 15],
    "BodyTemp": [96, 95, 98],
    "HeartRate": [55, 90, 75])
def test_valid_data_type():
    with pytest.raises(TypeError):
        data_validation(test_data_list)

# Test Case: empty data frame
empty_df = test_data.copy().iloc[0:0]
def test_empty_df():
    with pytest.raises(ValueError):
        data_validation(empty_df)

# Setup list of invalid data cases 
invalid_data_cases = []

# Case: missing "class" column
missing_target_col = test_data.copy()
missing_target_col = missing_target_col.drop("RiskLevel", axis=1)  # drop Risk Level target column
invalid_data_cases.append((missing_target_col, "RiskLevel from DataFrameSchema"))

# Case: label in target encoded numerically, instead of high, med, or low risk
wrong_risk_type = test_data.copy()
wrong_risk_type["RiskLevel"] = wrong_risk_type["RiskLevel"].map({'low risk': 0, 'med risk': 1, 'high risk': 2})
invalid_data_cases.append((wrong_risk_type, "Incorrect type in 'RiskLevel' column"))

# Case: wrong value in "RiskLevel" column
wrong_risk_label = test_data.copy()
wrong_risk_label.loc[0, "RiskLevel"] = "med-low risk"
invalid_data_cases.append((wrong_risk_label, "Incorrect category in 'RiskLevel' column"))

# Case: missing value in "RiskLevel" column
missing_risk = test_data.copy()
missing_risk.loc[0, "RiskLevel"] = None
invalid_data_cases.append((missing_risk, "Missing value in 'RiskLevel' column"))

# Case: missing column (one test for each column)
for col in test_data.columns:
    missing_col = test_data.copy()
    missing_col = missing_col.drop(col, axis=1)  # drop column
    invalid_data_cases.append((missing_col, f"'{col}' is missing from DataFrameSchema"))
    
# Generate a case for each column where data is too large
for col in test_data.columns:
    too_large = test_data.copy()
    too_large[col] = too_large[col] + 100  # Adding a high value to make it out of range
    invalid_data_cases.append((too_large, f"Check for values in '{col}' being too large, out of range"))

# Generate a case for each column where the data is too small
for col in test_data.columns:
    too_small = test_data.copy()
    too_small[col] = too_small[col] - 80  # Adding an arbitrary value to make it out of range
    invalid_data_cases.append((too_small, f"Check for values in '{col}' being too small, out of range"))

# Generate a case for each column where data is the wrong type
for col in test_data.columns:
    wrong_col_type = test_data.copy()
    wrong_col_type[col] = wrong_col_type[col].astype(str) # convert from numeric (int or float) to string
    invalid_data_cases.append((wrong_col_type, f"Check values in '{col}' should be of float or int type"))

# Case: entire row of missing values
empty_row_test = test_data.copy()
empty_row = pd.DataFrame([[np.nan] * (empty_row_test.shape[1] - 1) + [np.nan]], columns=empty_row_test.columns)
empty_row_test = pd.concat([empty_row_test, nan_row], ignore_index=True)
invalid_data_cases.append((empty_row_test, f"Check for missing observations (e.g., a row of all null values)"))

# Parameterize invalid data test cases
@pytest.mark.parametrize("invalid_data, description", invalid_data_cases)
def test_valid_w_invalid_data(invalid_data, description):
    with pytest.raises(pa.errors.SchemaErrors) as:
        data_validation(invalid_data)