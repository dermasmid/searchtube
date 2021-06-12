from pymongo import MongoClient
import os

def get_client():
    client = MongoClient('rextube_mongo', 27017, username=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'])
    return client
