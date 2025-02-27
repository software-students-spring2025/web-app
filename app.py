import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

@app.route("/")
def index():
    return "Hello World!"

#test route to see if MongoDB is connected to database use ip/test-db 
@app.route("/test-db")
def test_db():
    try:
        # Insert a new document with timestamp
        result = db.test_collection.insert_one(
            {"message": "Hello from Flask!", "timestamp": datetime.utcnow()}
        )
        
        # Retrieve the newly inserted document
        inserted_doc = db.test_collection.find_one({"_id": result.inserted_id}, {"_id": 0})

        return f"Inserted New Document: {inserted_doc}"
    except Exception as e:
        return f" Error inserting data: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
