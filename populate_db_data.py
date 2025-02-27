import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]


def populate_courses():
    """
    Populates the courses collection with sample data.
    """
    courses = [
        {
            "name": "Math 101",
        },
        {
            "name": "Physics 202",
        },
        {
            "name": "Chemistry 303",
        },
        {
            "name": "Biology 404",
        },
    ]

    db.courses.insert_many(courses)


if __name__ == "__main__":
    populate_courses()
