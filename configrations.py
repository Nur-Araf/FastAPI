from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

uri = os.getenv("MONGODB_URI")
print("MongoDB URI:", uri)  # Debugging line to check if the URI is loaded correctly

if not uri:
    raise Exception("MONGODB_URI is not set in the .env file")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.learning