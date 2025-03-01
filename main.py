from app import app

import pymongo
from bson.objectid import ObjectId
import datetime

from dotenv import load_dotenv
import os
load_dotenv()
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

db = client["test-database"]

collection = db.test_collection

# doc = {
#     "name": "Foo Barstein",
#     "email": "fb1258@nyu.edu",
#     "message": "We loved with a love that was more than love.\n -Edgar Allen Poe",
#     "created_at": datetime.datetime.utcnow() # the date time now
# }

# mongoid = collection.insert_one(doc)

docs = collection.find({
    "email": "fb1258@nyu.edu"
})
for doc in docs:
    # print(doc)
    output = '{name} ({email}) said "{message}" at {date}.'.format(
        name = doc['name'],
        email = doc['email'],
        message = doc['message'],
        date = doc['created_at'].strftime("%H:%M on %d %B %Y") # nicely-formatted datetime
    )
    print(output)