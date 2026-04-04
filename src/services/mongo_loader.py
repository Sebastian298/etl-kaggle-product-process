import logging
from typing import List, Dict, Any
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from src.config import Settings
from src.db.mongo_client import mongo_db

logger = logging.getLogger(__name__)


def load(data: List[Dict[str, Any]]) -> None:
    if not data:
        logger.info("No data to load.")
        return

    collection = mongo_db[Settings.mongo_collection_name]
    batch_size = Settings.csv_batch_size
    total_records = len(data)
    
    logger.info(f"Starting to load {total_records} records into MongoDB in batches of {batch_size}...")
    
    for i in range(0, total_records, batch_size):
        batch = data[i:i + batch_size]
        operations = []
        
        for item in batch:
            product_id = item.get("productId")
            if product_id is not None:
                operations.append(
                    UpdateOne(
                        {"productId": product_id},
                        {"$set": item},
                        upsert=True
                    )
                )
            else:
                logger.warning(f"Record skipped due to missing 'productId': {item}")
        
        if not operations:
            continue
            
        try:
            result = collection.bulk_write(operations, ordered=False)
            upserted = result.upserted_count
            modified = result.modified_count
            matched = result.matched_count
            logger.info(
                f"Batch {i // batch_size + 1}: Inserted (Upserts): {upserted}, "
                f"Updated: {modified}, Matched without changes: {matched - modified}"
            )
        except BulkWriteError as bwe:
            logger.error(f"Error writing to batch {i // batch_size + 1}: {bwe.details}")

    logger.info("Finished loading data to MongoDB.")
