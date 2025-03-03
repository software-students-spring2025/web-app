from dotenv import load_dotenv
import os
import pymongo

def get_db():
    load_dotenv()
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

    print(MONGO_URI)

    #make a connection to the database server
    connection = pymongo.MongoClient(MONGO_URI)
    db = connection["Jitter"]
    #g._database = db
    return db

