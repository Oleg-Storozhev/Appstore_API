import pymongo
from fastapi import HTTPException

from pymongo.errors import PyMongoError, ConnectionFailure
from service.tools.logger_file import logger
from typing import Mapping

from service.core.local_enviroments import (
    MONGO_CLIENT,
    MONGO_DB_NAME,
    MONGO_COLLECTION_NAME,
)


class MongoConnector:
    def __init__(self):
        try:
            self.mongo_db_collection = pymongo.MongoClient(MONGO_CLIENT)[MONGO_DB_NAME][MONGO_COLLECTION_NAME]
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise Exception("Failed to establish a connection to MongoDB")
        except Exception as e:
            logger.error(f"Unexpected error during MongoDB connection initialization: {e}")
            raise Exception("Unexpected error during MongoDB connection initialization")

    def convert_to_dict(self, obj):
        if isinstance(obj, Mapping):
            return dict(obj)
        return obj

    def get_data(self, app_name: str, app_id: str) -> dict:
        try:
            filter_query = {
                "$and": [
                    {"app_name": app_name},
                    {"app_id": app_id}
                ]
            }
            results = self.mongo_db_collection.find_one(filter=filter_query)
            if not results:
                logger.warning(f"No data found for app_name: {app_name}, app_id: {app_id}")
                return {}

            return self.convert_to_dict(results)

        except PyMongoError as e:
            logger.error(f"Error while retrieving data from MongoDB: {e}")
            raise HTTPException(status_code=503, detail="Error while retrieving data from MongoDB")
        except KeyError as e:
            logger.error(f"Missing key in the data dictionary: {e}")
            raise HTTPException(status_code=404, detail="Missing key in the data dictionary.")
        except Exception as e:
            logger.error(f"Unexpected error while retrieving data: {e}")
            raise Exception("Unexpected error while retrieving data")

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
        except PyMongoError as e:
            logger.error(f"Error while adding/updating data to MongoDB: {e}")
            raise HTTPException(status_code=503, detail="Error while adding/updating data to MongoDB")
        except KeyError as e:
            logger.error(f"Missing key in the data dictionary: {e}")
            raise HTTPException(status_code=404, detail="Missing key in the data dictionary.")
        except Exception as e:
            logger.error(f"Unexpected error while adding/updating data: {e}")
            raise Exception("Unexpected error while adding/updating data")
