import pytest
from unittest.mock import patch, MagicMock
from src.services.mongo_loader import load

def test_load_empty_data() -> None:
    load([])
    assert True

@patch('src.services.mongo_loader.mongo_db')
def test_load_with_data(mock_db: MagicMock) -> None:
    mock_collection = MagicMock()
    mock_db.return_value = mock_collection
    
    data = [
        {"productId": "123", "name": "Shirt", "price": 10},
        {"productId": "456", "name": "Pants"}
    ]
    
    try:
         load(data)
    except Exception as e:
         pytest.fail(f"load() raised an exception: {e}")
