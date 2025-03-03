"""Module to connnect with MongoDB database."""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

try:
    mongo_uri = "mongodb://localhost:27017/travel_match_db"  # Hardcoded local URI for testing
    client = MongoClient(mongo_uri)
    db = client.travel_match_db
    print("Connected to MongoDB!")
except ConnectionError as e:
    print("Failed to connect to MongoDB:", e)
