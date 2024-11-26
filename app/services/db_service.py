# MongoDB
from app.configs.db import mongo

def check_and_create_collection(collection_name):
    """Check if the collection exists, create it if not.
    
    Args:
        collection_name (str): The name of the collection to check and create.
        
    Returns:
        bool: True if the collection was created, False if it already exists.
    """
    if collection_name not in mongo.db.list_collection_names():
        mongo.db.create_collection(collection_name)
        return True
    else:
        return False


def check_collection(collection_name):
    """Check if the collection exists.
    
    Args:
        collection_name (str): The name of the collection to check.
        
    Returns:
        bool: True if the collection exists, False otherwise.
    """
    return collection_name in mongo.db.list_collection_names()

