# download_data.py
# author: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim
# date: 2024-12-14

import click
import os
import sys
import logging
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip


# Set up logging for better error handling and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.command()
@click.option('--url', type = str, help = "URL of dataset to be downloaded", required = True)
@click.option('--write_to', type = str, help = "Path to directory where raw data will be written to", required = True)
def main(url, write_to):
    """Downloads zip data from the web to a local filepath and extracts it."""
    try:
        os.makedirs(write_to, exist_ok = True)
        logging.info(f"Starting the process to download and extract data from {url} to {write_to}...")
        read_zip(url, write_to)
        logging.info(f"Data successfully downloaded and extracted to {write_to}")
        
    except ValueError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
