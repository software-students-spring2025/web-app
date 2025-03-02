from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,     # Add this
    url_for 
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
reviews_collection = db["reviews"] 

# ✅ Home Route - Render the homepage
@app.route("/")
def index():
    restaurants = list(
        restaurants_collection.find({}, {"_id": 0})
    )  # Fetch restaurants from MongoDB
    recent_reviews = list(
        reviews_collection.find().sort("created_at", -1).limit(5)
    )
    return render_template(
        "index.html", restaurants=restaurants, recent_reviews=recent_reviews
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

@app.route("/add-review", methods=["GET"])
def add_review_form():
    # Simply render the add_review.html template when users visit the page
    return render_template("add_review.html")

@app.route("/add-review", methods=["POST"])
def add_review():
    if request.method == "POST":
        # Extract data from the form submission
        restaurant_name = request.form.get("restaurant_name")  # Get restaurant name from form
        rating = int(request.form.get("rating"))               # Get rating and convert to integer
        review_text = request.form.get("review_text")          # Get the text of the review
        
        # Basic validation to ensure we have required data
        if not restaurant_name:
            return "Please provide a restaurant name", 400  # Return 400 Bad Request if no restaurant name
        
        if rating < 1 or rating > 5:
            return "Rating must be between 1 and 5", 400    # Ensure rating is between 1-5
            
        # Create a dictionary to represent the new review document for MongoDB
        new_review = {
            "restaurant_name": restaurant_name,  # Store restaurant name
            "rating": rating,                    # Store the numerical rating
            "review_text": review_text,          # Store the review content
            "created_at": datetime.datetime.now()         # Add a timestamp for when review was created
        }
        
        # Insert the review into reviews collection
        reviews_collection.insert_one(new_review)
        
        # Check if the restaurant exists and update or create it
        existing_restaurant = restaurants_collection.find_one({"name": restaurant_name})
        
        if existing_restaurant:
            # If the restaurant exists, update it to add this review to its reviews list
            restaurants_collection.update_one(
                {"name": restaurant_name},
                {"$push": {"reviews": new_review}}
            )
        else:
            # If the restaurant doesn't exist, create a new entry
            new_restaurant = {
                "name": restaurant_name,
                "rating": float(rating),
                "reviews": [new_review],
                "created_at": datetime.datetime.now()
            }
            restaurants_collection.insert_one(new_restaurant)
        
        # After successful insertion, redirect user back to home page
        return redirect(url_for("index"))
# ✅ Start Flask Application
if __name__ == "__main__":
    app.run(debug=True)
