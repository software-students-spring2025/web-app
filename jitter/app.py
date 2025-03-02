from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)

# Load environment variables
load_dotenv()

connection = pymongo.MongoClient(
    os.getenv("MONGO_URI")
)
db = connection["Jitter"]
restaurants_collection = db["restaurants"]


# ✅ Home Route - Render the homepage
@app.route("/")
def index():
    restaurants = list(
        restaurants_collection.find({}, {"_id": 0})
    )  # Fetch restaurants from MongoDB
    return render_template(
        "index.html", restaurants=restaurants
    )  # FIX: render_template now works!


# ✅ API - Add a restaurant
@app.route("/add_restaurant", methods=["POST"])
def add_restaurant():
    data = (
        request.json
        if request.content_type == "application/json"
        else request.form.to_dict()
    )

    if not data or "name" not in data or "rating" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_restaurant = {
        "name": data["name"],
        "rating": float(data["rating"]),
        "price": data.get("price", 0),
        "description": data.get("description", ""),
        "image_url": data.get("image_url", "https://via.placeholder.com/200"),
    }

    restaurants_collection.insert_one(new_restaurant)
    return jsonify({"message": "Restaurant added successfully"}), 201


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")  # Get search term from the form

    if not query:
        return "No search term provided", 400

    # Find the restaurant in MongoDB (case-insensitive search)
    restaurant = restaurants_collection.find_one(
        {"name": {"$regex": query, "$options": "i"}}
    )

    if not restaurant:
        return "Restaurant not found", 404

    # Extract reviews list (or empty list if none exist)
    reviews = restaurant.get("reviews", [])

    return render_template("reviews.html", restaurant=restaurant, reviews=reviews)

# ✅ Profile Page
@app.route("/profile")
def profile():
    return render_template("profile.html")  # FIX: render_template works now!


# ✅ Start Flask Application
if __name__ == "__main__":
    app.run(debug=True)
