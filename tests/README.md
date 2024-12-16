## Test Suite Developer Notes

### Running the Tests

Tests are run using the `pytest` command from the root of the project.

### Preparation of Test Zip Files

These files need to exist in the remote GitHub repository for the tests to pass - empty_test.zip, files_json_and_csv.zip, files_with_nested.zip. If one of them missing, run the create_files.py with the command `python tests/create_files.py` from the root directory. 