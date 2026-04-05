import re
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
