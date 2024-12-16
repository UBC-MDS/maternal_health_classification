import os
import zipfile
import requests

def read_zip(url, directory):
    """
    Read a zip file from the given URL and extract its contents to the specified directory,
    replacing any existing files in the directory if necessary.

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

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_file_contents = zip_ref.namelist()

            # Check if the zip file is empty
            if not zip_file_contents:
                raise ValueError('The ZIP file is empty or contains no new files.')

            # Clear existing files in the directory that match zip file contents
            for file_name in zip_file_contents:
                file_path = os.path.join(directory, file_name)
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)

            # Extract the zip file
            zip_ref.extractall(directory)
    except zipfile.BadZipFile:
        raise ValueError('The provided file is not a valid zip file.')


    print(f"Extraction successful! Extracted files: {zip_file_contents}")
