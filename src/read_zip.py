import os
import zipfile
import requests

def read_zip(url, directory):
    """
    Read a zip file from the given URL and extract its contents to the specified directory.

    Parameters:
    ----------
    url : str
        The URL of the zip file to be read.
    directory : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None
    """

    if not os.path.isdir(directory):
        raise ValueError('The directory provided does not exist.')

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('The URL provided does not exist.')

    filename = os.path.basename(url)
    if not filename.endswith('.zip'):
        raise ValueError('The URL provided does not point to a zip file.')

    zip_path = os.path.join(directory, filename)
    with open(zip_path, 'wb') as file:
        file.write(response.content)

    original_contents = set(os.listdir(directory))

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(directory)
    except zipfile.BadZipFile:
        raise ValueError('The provided file is not a valid zip file.')

    current_contents = set(os.listdir(directory))
    extracted_files = current_contents - original_contents
    if not extracted_files:
        raise ValueError('The ZIP file is empty or contains no new files.')

    os.remove(zip_path)

    print(f"Extraction successful! Extracted files: {extracted_files}")