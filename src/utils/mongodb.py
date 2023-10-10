import os
import sys
sys.path.append(os.getcwd())

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import polars as pl
import datetime
from dotenv import load_dotenv
load_dotenv()


class MongoDB():
    uri = os.getenv('MONGO_URI')

    def __init__(self) -> None:
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
    
    def insert(self) -> None:
        db = self.client.topic2 # Database
        ty_gia_collection = db.ty_gia # Collection
        
        df = pl.read_csv(os.path.join(os.getcwd(), 'results', 'exchange_rate.csv'))
        
        print(df)
        
        data_today = []
        
        for row in df.rows(named=True):
            new_data = {
                'date': row['Date'],
                'data': {
                    'dollar_index_dxy': row['Dollar Index DXY'],
                    'usd/vnd': {
                        'vcb_sell': row['USD/VND - VCB (sell)'],
                        'nhnn_sell':  row['USD/VND - NHNN (sell)'],
                    },
                    'eur/vnd': {
                        'vcb_sell': row['EUR/VND - VCB (sell)'],
                        'nhnn_sell':  row['EUR/VND - NHNN (sell)'],
                    },
                    'cny/vnd': {
                        'vcb_sell': row['CNY/VND - VCB (sell)'],
                        'nhnn_sell':  row['CNY/VND - NHNN (sell)'],
                    }
                }
            }
            
            data_today.append(new_data)
            
        print(ty_gia_collection.insert_many(data_today))

    def query(self) -> None:
        db = self.client.topic2
        ty_gia_collection = db.ty_gia
        
        print(ty_gia_collection.find_one({"date": "10/10/2023"}))
        print(ty_gia_collection.find_one({"date": "9/10/2023"}))

if __name__ == '__main__':
    mongo = MongoDB()
    # mongo.insert()
    mongo.query()