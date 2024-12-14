import pytest
import os
import shutil
import responses
import sys
import zipfile
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

# Test files setup
if not os.path.exists('tests/test_zip_data1'):
    os.makedirs('tests/test_zip_data1')

if not os.path.exists('tests/test_zip_data2'):
    os.makedirs('tests/test_zip_data2')
with open('tests/test_zip_data2/test4.txt', 'w') as file:
    pass  # Empty file for testing

with zipfile.ZipFile('tests/empty_test.zip', 'w') as zipf:
    pass

test_files_json = ['file5.json', 'nested_dir/file4.csv']
test_files_mixed = ['file1.txt', 'file2.csv', 'nested_dir/file3.txt', 'nested_dir/file4.csv']
test_files_nested = ['nested_dir/file3.txt', 'nested_dir/file4.csv']
test_files_duplicate = ['nested_dir/file3.txt', 'nested_dir/file3.txt']

def create_test_files(test_files):
    for file_path in test_files:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"Sample content for {file_path}\n")
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

create_test_files(test_files_json)
create_test_files(test_files_mixed)
create_test_files(test_files_nested)
create_test_files(test_files_duplicate)


url_json_zip = 'https://github.com/UBC-MDS/maternal_health_classification/raw/main/tests/files_json_and_csv.zip'  
url_mixed_zip = 'https://github.com/UBC-MDS/maternal_health_classification/raw/main/tests/files_with_nested.zip'
url_empty_zip = 'https://github.com/UBC-MDS/maternal_health_classification/raw/main/tests/empty_test.zip'
url_invalid_zip = 'https://example.com/invalid.zip'

# Mock non-existing URL
@pytest.fixture
def mock_response():
    # Mock a response with a non-200 status code
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, url_invalid_zip, status=404)
        yield

# Tests

# Test case 1: Zip containing only JSON files
def test_read_zip_json_files():
    read_zip(url_json_zip, 'tests/test_zip_data1')
    # Check if both file5.json and nested_dir/file4.csv are extracted
    for file in ['file5.json', 'nested_dir/file4.csv']:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)

# Test case 2: Zip with both files and nested directories
def test_read_zip_mixed_files_and_subdirectories():
    read_zip(url_mixed_zip, 'tests/test_zip_data1')
    for file in test_files_mixed:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)
    for file in test_files_mixed:
        if os.path.exists(file):
            os.remove(file)

# Test case 3: Zip with only nested directories (no files at the top level)
def test_read_zip_only_nested_dirs():
    with zipfile.ZipFile('nested_only.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('nested_dir/file3.txt')
        zipf.write('nested_dir/file4.csv')
    
    read_zip('nested_only.zip', 'tests/test_zip_data1')
    for file in test_files_nested:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)
    for file in test_files_nested:
        if os.path.exists(file):
            os.remove(file)

# Test case 4: Test empty zip file
def test_read_zip_empty_zip():
    with pytest.raises(ValueError, match='The ZIP file is empty.'):
        read_zip(url_empty_zip, 'tests/test_zip_data1')

# Test case 5: Test zip with duplicate files
def test_read_zip_duplicate_files():
    create_nested_dirs()  # Ensure the directory and file exist before zipping
    
    # Create a zip file containing the same file twice
    with zipfile.ZipFile('duplicate_files.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('nested_dir/file3.txt', arcname='nested_dir/file3.txt')
        zipf.write('nested_dir/file3.txt', arcname='nested_dir/file3.txt')  # Adding the same file again
    
    # Call the function to read the zip file
    read_zip('duplicate_files.zip', 'tests/test_zip_data1')
    
    # Check if only one file exists (no duplication)
    file_path = os.path.join('tests/test_zip_data1', 'nested_dir/file3.txt')
    assert os.path.isfile(file_path)

# Test case 6: Test invalid URL with 404 error
def test_read_zip_error_on_invalid_url(mock_response):
    with pytest.raises(ValueError, match='The URL provided does not exist.'):
        read_zip(url_invalid_zip, 'tests/test_zip_data1')

# Test case 7: Test zip file is not a zip file
def test_read_zip_error_on_nonzip_url():
    with pytest.raises(ValueError, match='The URL provided does not point to a zip file.'):
        read_zip('https://github.com/', 'tests/test_zip_data1')

# Test case 8: Test read_zip throws error when the directory path doesn't exist
def test_read_zip_error_on_missing_dir():
    with pytest.raises(ValueError, match='The directory provided does not exist.'):
        read_zip(url_json_zip, 'tests/test_zip_data3')

