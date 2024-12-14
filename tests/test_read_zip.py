import pytest
import os
import shutil
import responses
import sys
import zipfile
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

# Test files setup
if not os.path.exists('tests/test_zip_data1'):
    os.makedirs('tests/test_zip_data1')

if not os.path.exists('tests/test_zip_data2'):
    os.makedirs('tests/test_zip_data2')
with open('tests/test_zip_data2/test4.txt', 'w') as file:
    pass  # Empty file for testing

test_files_json = ['file5.json', 'nested_dir/file4.csv']  # Include both files from `files_json_and_csv.zip`
test_files_mixed = ['file1.txt', 'file2.csv', 'nested_dir/file3.txt', 'nested_dir/file4.csv']
test_files_nested = ['nested_dir/file3.txt', 'nested_dir/file4.csv']
test_files_duplicate = ['nested_dir/file3.txt', 'nested_dir/file3.txt']

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


@pytest.fixture
def mock_urls():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET, url_json_zip, body=open('tests/files_json_and_csv.zip', 'rb').read(), status=200
        )
        rsps.add(
            responses.GET, url_mixed_zip, body=open('tests/files_with_nested.zip', 'rb').read(), status=200
        )
        rsps.add(
            responses.GET, url_empty_zip, body=open('tests/empty_test.zip', 'rb').read(), status=200
        )
        yield rsps

# Ensure the directories exist before writing to them
def create_nested_dirs():
    os.makedirs('nested_dir', exist_ok=True)

# Tests

# Test case 1: Zip containing only JSON files
def test_read_zip_json_files(mock_urls):
    read_zip(url_json_zip, 'tests/test_zip_data1')
    # Check if both file5.json and nested_dir/file4.csv are extracted
    for file in ['file5.json', 'nested_dir/file4.csv']:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)

# Test case 2: Zip with both files and nested directories
def test_read_zip_mixed_files_and_subdirectories(mock_urls):
    read_zip(url_mixed_zip, 'tests/test_zip_data1')
    for file in test_files_mixed:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)
    for file in test_files_mixed:
        if os.path.exists(file):
            os.remove(file)

# Test case 3: Zip with only nested directories (no files at the top level)
def test_read_zip_only_nested_dirs(mock_urls):
    create_nested_dirs()  # Ensure nested_dir exists
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
def test_read_zip_empty_zip(mock_urls):
    with pytest.raises(ValueError, match='The ZIP file is empty.'):
        read_zip(url_empty_zip, 'tests/test_zip_data1')

# Test case 5: Test zip with duplicate files
def test_read_zip_duplicate_files(mock_urls):
    create_nested_dirs()  # Ensure nested_dir exists
    with zipfile.ZipFile('duplicate_files.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('nested_dir/file3.txt')
        zipf.write('nested_dir/file3.txt')  # Adding the same file again
    
    read_zip('duplicate_files.zip', 'tests/test_zip_data1')
    # Check if only one file exists (no duplication)
    file_path = os.path.join('tests/test_zip_data1', 'nested_dir/file3.txt')
    assert os.path.isfile(file_path)
    
    if os.path.exists('nested_dir/file3.txt'):
        os.remove('nested_dir/file3.txt')

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
