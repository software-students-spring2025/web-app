from bson.objectid import ObjectId
import datetime
import pymongo
import config
from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI')


MONGO_DBNAME = os.getenv('MONGO_DBNAME')

connection = MongoClient(MONGO_URI)
db = connection[MONGO_DBNAME]

reviews = db.reviews
