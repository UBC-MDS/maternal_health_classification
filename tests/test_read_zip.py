import pytest
import os
import shutil
import responses
import sys
import zipfile
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

if os.path.exists('tests/test_zip_data'):
    shutil.rmtree('tests/test_zip_data')
os.makedirs('tests/test_zip_data')

url_json_zip = 'https://example.org/files_json_and_csv.zip'  
url_mixed_zip = 'https://example.org/files_with_nested.zip'
url_empty_zip = 'https://example.org/empty_test.zip'
url_invalid_zip = 'https://example.org//invalid.zip'

# Mock non-existing URL
@pytest.fixture
def mock_response():
    # Mock a response with a non-200 status code
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, url_invalid_zip, status=404)
        yield


@pytest.fixture
def mock_urls():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
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

# Tests

def test_read_zip_json_files(mock_urls):
    read_zip(url_json_zip, 'tests/test_zip_data')
    for file in ['test.json', 'test.csv']:
        file_path = os.path.join('tests/test_zip_data', file)
        assert os.path.isfile(file_path)

def test_read_zip_mixed_files_and_subdirectories(mock_urls):
    read_zip(url_mixed_zip, 'tests/test_zip_data')
    test_files_mixed = ['nested_dir/file3.txt', 'nested_dir/file4.csv']
    for file in test_files_mixed:
        file_path = os.path.join('tests/test_zip_data', file)
        assert os.path.isfile(file_path)

def test_read_zip_empty_zip(mock_urls):
    with pytest.raises(ValueError, match='The ZIP file is empty or contains no new files.'):
        read_zip(url_empty_zip, 'tests/test_zip_data')

def test_read_zip_error_on_invalid_url(mock_response):
    with pytest.raises(ValueError, match='The URL provided does not exist.'):
        read_zip(url_invalid_zip, 'tests/test_zip_data')

def test_read_zip_error_on_nonzip_url():
    with pytest.raises(ValueError, match='The URL provided does not point to a zip file.'):
        read_zip('https://github.com/', 'tests/test_zip_data')
