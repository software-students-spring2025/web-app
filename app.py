from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


# load environment variables
load_dotenv()

app = Flask(__name__)

# secret key generation
secret_key = os.urandom(12)
app.config["SECRET_KEY"] = secret_key

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("Cluster0")

bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Collections
pins_collection = db.pins
bathrooms_collection = db.bathrooms
reviews_collection = db.reviews
users_collection = db.users

class User(UserMixin):
    def __init__(self, user_id, email, is_admin):
        self.id = str(user_id)  # Ensure it is a string
        self.email = email
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})  # Convert back to ObjectId
    if user:
        return User(user_id=str(user["_id"]), email=user["email"], is_admin=user["is_admin"])
    return None



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))  # Redirect if already logged in

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(user_id=str(user["_id"]), email=user["email"], is_admin=user["is_admin"])
            login_user(user_obj, remember=True)  # Ensure session persists

            session["user_id"] = str(user["_id"])  # Store user in session
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@app.route("/debug") # for debugging user accounts
def debug():
    if current_user.is_authenticated:
        return f"Logged in as: {current_user.email}, Admin: {current_user.is_admin}"
    return "Not logged in"


@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    is_admin = "admin_privileges" in request.form  # Checkbox in form

    if not email.endswith("@nyu.edu"):
        flash("You must use an NYU email to register!", "danger")
        return redirect(url_for("login"))

    if users_collection.find_one({"email": email}):
        flash("Email already exists!", "danger")
        return redirect(url_for("login"))

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({"email": email, "password": hashed_password, "is_admin": is_admin})
    
    flash("Account created! You can now log in.", "success")
    return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("home.html", is_admin=current_user.is_admin)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/bathroom/<bathroomID>")
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

@app.route('/api/pins')
def get_pins():
    pins = list(db.pins.find({}, {"_id": 1, "name": 1, "lat": 1, "lng": 1}))  # Explicitly include _id

    # Convert MongoDB ObjectId to a string for JSON compatibility
    for pin in pins:
        pin['_id'] = str(pin['_id'])

    return jsonify(pins)

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
    floor_filter = request.args.get("floor")
    type_filter = request.args.get("type")

    # fetch building by name (case-insensitive)
    building = pins_collection.find_one({"name": {"$regex": query, "$options": "i"}})

    # return empty list of bathrooms if no building found
    if not building:
        return jsonify({"bathrooms": []})
    
    bathroom_query = {"location_id": building["_id"]}

    if floor_filter:
        bathroom_query["floor"] = int(floor_filter)  # Convert to integer
    if type_filter:
        bathroom_query["type"] = type_filter  # Match bathroom type

    # Fetch bathrooms that match filters
    bathrooms = list(bathrooms_collection.find(bathroom_query))

    # convert ObjectId fields to string
    building = convert_objectid(building)
    bathrooms = convert_objectid(bathrooms)

    # return bathrooms list as the response
    return jsonify({"bathrooms": bathrooms})

@app.route("/building/<building_id>")
def view_building(building_id):
    # Fetch building details
    building = pins_collection.find_one({"_id": ObjectId(building_id)})

    if not building:
        return "Building not found", 404

    # Fetch bathrooms associated with this building
    bathrooms = list(bathrooms_collection.find({"location_id": ObjectId(building_id)}))

    return render_template("building.html", building=building, bathrooms=bathrooms)

if __name__ == "__main__":
    app.run(debug=True)
