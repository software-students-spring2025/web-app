import pymongo

# make a connection to the database server
connection = pymongo.MongoClient("mongodb://admin:secret@127.0.0.1:27017")

# select a specific database on the server
db = connection["mongodb_dockerhub"]

def get_tasks():
    collection = db["taskmanager"]
    return collection.find()


def add_task(task):
    collection = db["taskmanager"]
    collection.insert_one({"title":task["title"], "description":task["description"], "status":task["status"]})

