from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("Cluster0")

# Collections
pins_collection = db.pins
bathrooms_collection = db.bathrooms

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/api/pins")
def get_pins():
    # fetch all pins from MongoDB
    pins = list(pins_collection.find({}, {"_id": 0, "name": 1, "lat": 1, "lng": 1}))
    return jsonify(pins)

from bson import ObjectId

# helper function, converts ObjectId to string
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    else:
        return obj

@app.route("/api/search", methods=["GET"])
def search_api():
    query = request.args.get("q", "").lower()

    # fetch building by name (case-insensitive)
    building = pins_collection.find_one({"name": {"$regex": query, "$options": "i"}})

    # return empty list of bathrooms if no building found
    if not building:
        return jsonify({"bathrooms": []})

    # fetch bathrooms associated w/ found building
    bathrooms = list(bathrooms_collection.find({"location_id": building["_id"]}))

    # convert ObjectId fields to string
    building = convert_objectid(building)
    bathrooms = convert_objectid(bathrooms)

    # return bathrooms list as the response
    return jsonify({"bathrooms": bathrooms})

if __name__ == "__main__":
    app.run(debug=True)
