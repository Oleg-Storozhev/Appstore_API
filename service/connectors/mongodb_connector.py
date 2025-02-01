import pymongo

from service.core.local_enviroments import (
    MONGO_CLIENT,
    MONGO_DB_NAME,
    MONGO_COLLECTION_NAME,
)
from service.tools.logger_file import logger


class MongoConnector:
    def __init__(self):
        self.mongo_db_collection = pymongo.MongoClient(MONGO_CLIENT)[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

    def get_data(self, app_name: str, app_id: str) -> dict:
        filter_query = {
            "$and": [
                {"app_name": app_name},
                {"app_id": app_id}
            ]
        }
        results = self.mongo_db_collection.find_one(filter=filter_query)
        return results

    def add_or_update_data(self, data: dict) -> None:
        try:
            filter_query = {
                "$and": [
                    {"app_name": data['app_name']},
                    {"app_id": data['app_id']}
                ]
            }
            self.mongo_db_collection.update_one(
                filter=filter_query,
                update={"$set": data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error while adding/updating data to MongoDB: {e}")
