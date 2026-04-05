import logging
import pandas as pd
from typing import List, Dict, Any

from src.mappers.product_mapper import map_csv_row_to_dto, map_dto_to_dict

logger = logging.getLogger(__name__)

def transform(csv_file_path: str) -> List[Dict[str, Any]]:
    """
    Reads the designated CSV file using pandas, iteratively maps rows
    to DTOs, and outputs serializable dictionaries.
    
    Args:
        csv_file_path (str): Full absolute or relative path to the source CSV file.
        
    Returns:
        List[Dict[str, Any]]: Transformed data mapped to camelCase layout and prepared 
            for the DB loader. Returns an empty list upon failure.
    """
    logger.info(f"Starting transformation of file: {csv_file_path}")
    
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {csv_file_path}")
        return []
    except Exception as e:
        logger.error(f"Fatal error reading CSV file: {e}")
        return []
        
    records: List[Dict[str, Any]] = []
    
    # Iteratively map the dataset.
    for index, row in df.iterrows():
        try:
            dto = map_csv_row_to_dto(row)
            record_dict = map_dto_to_dict(dto)
            records.append(record_dict)
        except Exception as e:
            logger.warning(
                f"Error transforming row index {index} "
                f"(Product ID: {row.get('product_id', 'Unknown')}): {e}"
            )
            
    logger.info(f"Successfully transformed {len(records)} mapping records.")
    return records
