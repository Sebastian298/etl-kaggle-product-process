import os
from src.config import Settings

# Importing the kaggle module will implicitly read KAGGLE_USERNAME and KAGGLE_KEY
# from the environment variables, which were just loaded by dotenv in config.py
import kaggle

def extract(
    dataset_name: str = Settings.kaggle_dataset, 
    output_dir: str = Settings.csv_input_dir
) -> None:
    """
    Authenticate to Kaggle and download the designated dataset CSV files.

    This function authenticates using the environment variables KAGGLE_USERNAME 
    and KAGGLE_KEY, which are loaded via the project configuration settings. 
    It downloads the dataset and extracts it to the specified output directory.

    Args:
        dataset_name (str): The name of the Kaggle dataset to download. Defaults to 
            the dataset defined in settings.
        output_dir (str): The local directory to save the extracted data to. Defaults to
            the raw data directory defined in settings.

    Returns:
        None
    """
    if not dataset_name:
        raise ValueError("Dataset name must be provided")
    
    if not output_dir:
        raise ValueError("Output directory must be provided")

    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Authenticating and downloading dataset '{dataset_name}' to '{output_dir}'...")
    
    # Authenticate using the environment variables loaded in config.py
    kaggle.api.authenticate()
    
    # Download the dataset and automatically unzip its contents
    kaggle.api.dataset_download_files(dataset_name, path=output_dir, unzip=True)
    
    print("Download and extraction completed successfully.")
