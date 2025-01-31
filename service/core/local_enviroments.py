import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
HF_KEY = os.getenv("HF_KEY")

MONGO_CLIENT = os.getenv("MONGO_CLIENT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")