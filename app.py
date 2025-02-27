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
reviews_collection = db.reviews

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")



@app.route("/bathroom/<bathroomID>.html")
def bathroom(bathroomID):
    bathroom = bathrooms_collection.find_one({"_id": ObjectId(bathroomID)})
    bathroomName=pins_collection.find_one({"_id":bathroom.get("location_id")}).get("name")
    fullLocation = bathroomName+", Floor "+str(bathroom.get("floor"))
    description=bathroom.get("type")+" "+bathroom.get("orientation")+" Bathroom"
    reviews = reviews_collection.find({"bathroom_id": ObjectId(bathroomID)})
    imageURL=str(bathroom.get("img_url"))
    if (imageURL=="None" or imageURL==""):
        imageString="Image Not Found"
    else:
        imageString="<img src='"+imageURL+"'>"
    i=0
    revSum=0
    for review in reviews:
        i+=1
        revSum+=review["rating"]
    revSum=revSum/i
    overallRating=""
    i=0
    while (i<revSum):
        i+=1
        if i>revSum:
            overallRating+="<i class='fa-solid fa-star-half-stroke'></i>"
        else:
            overallRating+="<i class='fa-solid fa-star'></i>"
    while (i<5):
        i+=1
        overallRating +="<i class='fa-regular fa-star'></i>"
    reviews = reviews_collection.find({"bathroom_id": ObjectId(bathroomID)})
    print(reviews)
    return render_template("bathroom.html",rating=overallRating,bathroomDescription=description, bathroomLocation=fullLocation,toilets=str(bathroom.get("toilets")),bathroomImage=imageString,bathroomReviews=reviews,sinks=str(bathroom.get("sinks")))


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
