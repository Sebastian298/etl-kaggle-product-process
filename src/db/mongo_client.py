import urllib.parse
from pymongo import MongoClient

from src.config import Settings


def get_mongo_client() -> MongoClient:
    """
    Creates and returns a MongoClient instance using configurations from Settings.
    Handles credentials in the connection URI securely.
    
    Returns:
        MongoClient: MongoDB connection client.
    """
    username = urllib.parse.quote_plus(Settings.mongo_username or "")
    password = urllib.parse.quote_plus(Settings.mongo_password or "")
    
    if username and password:
        uri = f"mongodb://{username}:{password}@{Settings.mongo_host}:{Settings.mongo_port}/?authSource={Settings.mongo_db_name}"
    else:
        uri = f"mongodb://{Settings.mongo_host}:{Settings.mongo_port}/"

    client = MongoClient(uri)
    return client


mongo_client = get_mongo_client()
mongo_db = mongo_client[Settings.mongo_db_name]
