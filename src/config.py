import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    csv_input_dir = os.getenv("CSV_INPUT_DIR")
    csv_batch_size = 500
    csv_encoding = "utf-8"

    kaggle_dataset = os.getenv("KAGGLE_DATASET")

    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT"))
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME")