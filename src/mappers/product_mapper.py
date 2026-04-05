import pandas as pd
from typing import Dict, Any
from math import isnan

from src.dtos.product_dto import ProductDTO
from src.helpers.data_cleaners import clean_price

def clean_nan(val: Any) -> Any:
    """
    Replaces pandas NaN floats with None to avoid Pydantic validation errors.
    
    Args:
        val: Value from the DataFrame row.
        
    Returns:
        Any: Value mapped to None if it was NaN.
    """
    if isinstance(val, float) and isnan(val):
        return None
    return val

def map_csv_row_to_dto(row: pd.Series) -> ProductDTO:
    """
    Maps a raw CSV row (pandas Series) to a ProductDTO.
    
    Args:
        row: A row from a pandas DataFrame.
        
    Returns:
        ProductDTO: An instance mapped via standard cleanups.
    """
    row_dict = {k: clean_nan(v) for k, v in row.to_dict().items()}
    
    # Specifically process price fields which may contain raw currencies / strings.
    row_dict['final_price'] = clean_price(row_dict.get('final_price'))
    row_dict['initial_price'] = clean_price(row_dict.get('initial_price'))
    
    return ProductDTO(**row_dict)

def map_dto_to_dict(dto: ProductDTO) -> Dict[str, Any]:
    """
    Serializes a ProductDTO to a dictionary with camelCase keys 
    as expected by the MongoDB loader and excludes null fields.
    
    Args:
        dto: The ProductDTO object.
        
    Returns:
        Dict: JSON-compliant dictionary with camelCase syntax.
    """
    return dto.model_dump(by_alias=True, exclude_none=True)
