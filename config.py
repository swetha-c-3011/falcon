from pymongo import MongoClient

class MongoDBConfig:
    def __init__(self,uri="mongodb://localhost:27017/",db_name="userdb"):
        self.client=MongoClient(uri)
        self.db=self.client[db_name]

    def get_database(self):
        return self.db