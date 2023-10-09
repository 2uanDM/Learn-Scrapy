from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import datetime


class MongoDB():
    uri = "mongodb+srv://kaxim_stock2023:dZ3WBFQsZ3f8rCyK@topic2.0d3b4gx.mongodb.net/?retryWrites=true&w=majority"

    def __init__(self) -> None:
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
    
    def insert(self) -> None:
        db = self.client.topic2
        people = db.people
        
        personDocument = {
            "name": { "first": "Alan", "last": "Turing" },
            "birth": datetime.datetime(1912, 6, 23),
            "death": datetime.datetime(1954, 6, 7),
            "contribs": [ "Turing machine", "Turing test", "Turingery" ],
            "views": 1250000
        }
        
        print(people.insert_one(personDocument))

    def query(self) -> None:
        db = self.client.topic2
        people = db.people
        
        print(people.find_one({"name.last": "Turing"}))

if __name__ == '__main__':
    mongo = MongoDB()
    # mongo.insert()
    mongo.query()