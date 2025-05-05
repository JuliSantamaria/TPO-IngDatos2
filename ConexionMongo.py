from pymongo import MongoClient

def get_mongo_client():
    return MongoClient(
        "mongodb://localhost"
    )

def get_db():
    client = get_mongo_client()
    return client.tienda_deportes
