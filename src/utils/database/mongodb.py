import os
import sys
sys.path.append(os.getcwd())

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel, Field

import polars as pl
import datetime
from dotenv import load_dotenv
load_dotenv()


class MongoDB():
    uri = os.getenv('MONGO_URI')

    def __init__(self, cluster: str) -> None:
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        
        # Get the cluster
        self.db = self.client[cluster]
    
    def get_db(self):
        return self.db
    
    def update_collection(self, collection_name: str, data) -> None:
        collection = self.db[collection_name]
        if data.isinstance(data, list):
            collection.insert_many(data)
        elif data.isinstance(data, dict):
            collection.insert_one(data)
        else:
            raise ValueError('Data must be a list or a dict')

