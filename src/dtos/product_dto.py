from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class ProductDTO(BaseModel):
    """
    Data Transfer Object representing a single product from the dataset.
    Fields are styled in snake_case internally but serialize to camelCase 
    via the configured alias_generator.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )
    
    product_id: int
    title: Optional[str] = None
    product_description: Optional[str] = None
    rating: Optional[float] = None
    ratings_count: Optional[int] = None
    initial_price: Optional[float] = None
    discount: Optional[float] = None
    final_price: Optional[float] = None
    currency: Optional[str] = None
    images: Optional[str] = None
    delivery_options: Optional[str] = None
    product_details: Optional[str] = None
    breadcrumbs: Optional[str] = None
    product_specifications: Optional[str] = None
    amount_of_stars: Optional[str] = None
    what_customers_said: Optional[str] = None
    seller_name: Optional[str] = None
    sizes: Optional[str] = None
    videos: Optional[str] = None
    seller_information: Optional[str] = None
    variations: Optional[str] = None
    best_offer: Optional[str] = None
    more_offers: Optional[str] = None
    category: Optional[str] = None
