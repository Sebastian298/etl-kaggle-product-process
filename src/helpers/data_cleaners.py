import re
import json
from typing import Optional, Any

def clean_price(price_str: Any) -> Optional[float]:
    """
    Cleans a price string by removing currency symbols and commas, 
    and converts it to a float.
    
    Args:
        price_str: The raw price value from the CSV (could be string, float or None).
        
    Returns:
        Optional[float]: The cleaned numeric price, or None if invalid/empty.
    """
    if price_str is None:
        return None
        
    str_val = str(price_str)
    
    # Handle explicitly NaN as string passed from Pandas
    if str_val.lower() == 'nan':
        return None
        
    # Remove any characters excluding digits and dots
    cleaned = re.sub(r'[^\d.]', '', str_val)
    if not cleaned:
        return None
        
    try:
        return float(cleaned)
    except ValueError:
        return None

def parse_json_safely(json_str: Any) -> Any:
    """Safely decodes a JSON string."""
    if not isinstance(json_str, str) or str(json_str).lower() == 'nan':
        return None
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

def extract_sizes(sizes_str: Any) -> Optional[list]:
    """Extracts a list of size strings from the sizes JSON array."""
    parsed = parse_json_safely(sizes_str)
    if isinstance(parsed, list):
        return [item.get("size") for item in parsed if isinstance(item, dict) and "size" in item]
    return None

def extract_product_details_description(details_str: Any) -> Optional[str]:
    """Extracts only the 'description' value from the product_details JSON."""
    parsed = parse_json_safely(details_str)
    if isinstance(parsed, dict):
        return parsed.get("description")
    return None
