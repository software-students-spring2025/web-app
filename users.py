import pymongo
from app import db
from bson.objectid import ObjectId


user = {
    "name": "John Doe",
    "email": "jd1234@nyu.edu",
    "username": "jd1234",
    "password": "password1"
}