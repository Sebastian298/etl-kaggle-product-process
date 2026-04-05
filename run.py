import os
import logging

from src.config import Settings
from src.services.kaggle_extractor import extract
from src.services.transformer import transform
from src.services.mongo_loader import load

# Configure default Python logging output format and levels
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("MyntraETL")

def main() -> None:
    """
    Main Orchestrator Entry Point for the Pipeline.
    Manages the Extraction, Transformation, and Load processes synchronously.
    """
    logger.info("Initializing ETL Pipeline...")
    
    try:
        # Phase 1: Extractions
        logger.info("=== Phase 1: EXTRACTION ===")
        extract()
        
        # Searching the configured local cache directory for any CSV to process
        csv_input_dir = Settings.csv_input_dir
        if not os.path.exists(csv_input_dir):
            logger.error(f"Extraction directory not mapped properly: {csv_input_dir}")
            return
            
        csv_files = [f for f in os.listdir(csv_input_dir) if f.endswith('.csv')]
        
        if not csv_files:
            logger.error("No valid CSV files identified post-extraction. Halting pipeline.")
            return
            
        logger.info(f"Found {len(csv_files)} CSV files. Processing them sequentially.")
        
        for csv_file in csv_files:
            target_csv_file = os.path.join(csv_input_dir, csv_file)
            logger.info(f"--- Processing File: {csv_file} ---")
            
            # Phase 2: Transformation
            logger.info("=== Phase 2: TRANSFORMATION ===")
            transformed_payload = transform(target_csv_file)
            
            if not transformed_payload:
                logger.warning(f"No data produced during transformation for {csv_file}. Skipping to next.")
                continue
                
            # Phase 3: Data Load
            logger.info("=== Phase 3: LOAD ===")
            load(transformed_payload)
        
        logger.info("ETL Pipeline finalized securely.")
        
    except Exception as e:
        logger.critical(f"A catastrophic error triggered context teardown: {e}", exc_info=True)

if __name__ == "__main__":
    main()
