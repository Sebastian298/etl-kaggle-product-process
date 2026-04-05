import pytest
from unittest.mock import patch, MagicMock
from src.services.kaggle_extractor import extract

@patch("src.services.kaggle_extractor.kaggle.api")
@patch("src.services.kaggle_extractor.os.makedirs")
def test_extract_success(mock_makedirs: MagicMock, mock_kaggle_api: MagicMock) -> None:
    """
    Test successful execution of the extract function.
    Given valid arguments, it should attempt to authenticate and download the dataset.
    """
    test_dataset = "test-user/test-dataset"
    test_dir = "./test/data/raw"
    
    extract(dataset_name=test_dataset, output_dir=test_dir)
    
    # Verify directory creation is called
    mock_makedirs.assert_called_once_with(test_dir, exist_ok=True)
    
    # Verify kaggle auth and download were called
    mock_kaggle_api.authenticate.assert_called_once()
    mock_kaggle_api.dataset_download_files.assert_called_once_with(
        test_dataset, path=test_dir, unzip=True
    )

def test_extract_missing_dataset_name() -> None:
    """
    Test that extract raises ValueError when dataset name is None or empty.
    """
    with pytest.raises(ValueError, match="Dataset name must be provided"):
        extract(dataset_name="")

def test_extract_missing_output_dir() -> None:
    """
    Test that extract raises ValueError when output directory is None or empty.
    """
    with pytest.raises(ValueError, match="Output directory must be provided"):
        extract(dataset_name="some/dataset", output_dir="")
