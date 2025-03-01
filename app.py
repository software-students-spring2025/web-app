##Our Recipe Sharing App
import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

##FROM MONGO DB ATLAS
uri = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
