from pymongo import MongoClient
from dotenv import  load_dotenv
from loguru import logger

import threading
import os

load_dotenv()
class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self._init_mongo_connection()

    def _init_mongo_connection(self):
        try:
            self.MONGODB_SRV = os.getenv("MONGODB_SRV")

            self._mongo_client = MongoClient(self.MONGODB_SRV)
            self._mongo_client.admin.command("ping")

            logger.info("MongoDB connected")

        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise RuntimeError("MongoDB unavailable")
    
    def get_mongo_collection(self, db, collection):
        return self._mongo_client[db][collection]
