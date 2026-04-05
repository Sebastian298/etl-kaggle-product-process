import os
import logging
from unittest.mock import patch, MagicMock
from typing import List, Any

# Import the module under test
import run

def test_main_csv_dir_not_exists(caplog: Any) -> None:
    """
    Test the main function when the CSV input directory does not exist.
    It should call extract, log an error, and return early.
    """
    with patch("run.extract") as mock_extract, \
         patch("run.Settings.csv_input_dir", "/mock/input/dir"), \
         patch("run.os.path.exists", return_value=False) as mock_exists, \
         caplog.at_level(logging.ERROR):
        
        run.main()
        
        mock_extract.assert_called_once()
        mock_exists.assert_called_once_with("/mock/input/dir")
        assert "Extraction directory not mapped properly: /mock/input/dir" in caplog.text


def test_main_no_csv_files(caplog: Any) -> None:
    """
    Test the main function when the CSV input directory exists but contains no valid CSV files.
    It should call extract, find no CSV files, log an error, and return early.
    """
    with patch("run.extract") as mock_extract, \
         patch("run.Settings.csv_input_dir", "/mock/input/dir"), \
         patch("run.os.path.exists", return_value=True) as mock_exists, \
         patch("run.os.listdir", return_value=["test.txt", "data.json"]) as mock_listdir, \
         caplog.at_level(logging.ERROR):
        
        run.main()
        
        mock_extract.assert_called_once()
        mock_exists.assert_called_once_with("/mock/input/dir")
        mock_listdir.assert_called_once_with("/mock/input/dir")
        assert "No valid CSV files identified post-extraction. Halting pipeline." in caplog.text


def test_main_successful_pipeline_execution(caplog: Any) -> None:
    """
    Test a fully successful pipeline execution where CSV files are found,
    transformed, and loaded.
    """
    csv_files: List[str] = ["data1.csv", "data2.csv"]
    
    def mock_transform_side_effect(file_path: str) -> List[dict]:
        if "data1.csv" in file_path:
            return [{"id": 1, "name": "Item 1"}]
        return [] # Simulating data2 producing no payload

    with patch("run.extract") as mock_extract, \
         patch("run.Settings.csv_input_dir", "/mock/dir"), \
         patch("run.os.path.exists", return_value=True), \
         patch("run.os.listdir", return_value=["test.txt", "data1.csv", "data2.csv"]), \
         patch("run.transform", side_effect=mock_transform_side_effect) as mock_transform, \
         patch("run.load") as mock_load, \
         caplog.at_level(logging.INFO):
        
        run.main()
        
        mock_extract.assert_called_once()
        
        # transform should be called twice (for the two CSV files)
        assert mock_transform.call_count == 2
        mock_transform.assert_any_call(os.path.join("/mock/dir", "data1.csv"))
        mock_transform.assert_any_call(os.path.join("/mock/dir", "data2.csv"))
        
        # load should be called only once, for data1.csv because data2.csv produced empty payload
        mock_load.assert_called_once_with([{"id": 1, "name": "Item 1"}])
        
        assert "ETL Pipeline finalized securely." in caplog.text
        assert "No data produced during transformation for data2.csv. Skipping to next." in caplog.text


def test_main_catastrophic_error(caplog: Any) -> None:
    """
    Test the main function when an unexpected exception is raised during the pipeline.
    It should catch the exception and log a critical event.
    """
    with patch("run.extract", side_effect=ValueError("Test Exception")) as mock_extract, \
         caplog.at_level(logging.CRITICAL):
        
        run.main()
        
        mock_extract.assert_called_once()
        assert "A catastrophic error triggered context teardown: Test Exception" in caplog.text
