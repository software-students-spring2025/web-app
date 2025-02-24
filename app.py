import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from bson.objectid import ObjectId


load_dotenv("config.env")
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No MongoDB URI found in environment variables. Please set MONGO_URI.")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key") 


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = SECRET_KEY


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["users"]            
users_collection = db["users"]  


# default landing page: login 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = users_collection.find_one({"username": username})

        if not user:
            flash("Username not found. Please try again.", "error")
            return redirect(url_for("index"))
        
        if user['password'] != password:
            flash("Invalid password. Please try again.", "error")
            return redirect(url_for("index"))
        
        session['username'] = username
        return redirect(url_for("home"))
    
    return render_template("index.html")

# register page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        # Check if username exists
        if users_collection.find_one({"username": username}):
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for("signup"))
        
        # Check if passwords match
        if password != password2:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("signup"))
        
        # Insert new user into the database
        new_user = {"username": username, "password": password}
        users_collection.insert_one(new_user)
        session['username'] = username
        return redirect(url_for("home"))

    return render_template("signup.html")

# add dream page
from datetime import datetime
from bson import ObjectId

@app.route("/add_dream", methods=["GET", "POST"])
def add_dream():
    # Ensure the user is logged in
    if "username" not in session:
        flash("Please log in to add a dream.", "error")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        # Get date parts from the form
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        try:
            dream_date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
        except ValueError:
            flash("Invalid date provided. Please use valid day, month, and year.", "error")
            return redirect(url_for("add_dream"))
        
        # Get the dream description
        description = request.form.get("dream-description")
        
        # Optionally, get the tags from a hidden input or a comma-separated string
        tags_str = request.form.get("tags", "")
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
        
        # Construct a new dream object
        dream_data = {
            "date": dream_date,
            "description": description,
            "tags": tags
        }
        
        username = session.get("username")
        result = users_collection.update_one(
            {"username": username},
            {"$push": {"dreams": dream_data}}
        )
        
        if result.modified_count:
            flash("Dream added successfully!", "success")
        else:
            flash("Failed to add dream. Please try again.", "error")
        
        # Redirect back to add_dream page so notifications appear there
        return redirect(url_for("add_dream"))
    
    return render_template("add_dream.html")





# home page
@app.route("/home")
def home():
    user = session.get('username')
    return render_template("home.html", username=user)

# analysis page
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

#edit_dream page
@app.route("/edit_dream")
def edit_dream():
    tags = ["Happy", "Funny", "Excited", "XXXX"]
    return render_template("edit_dream.html", tags=tags)

if __name__ == "__main__":
    app.run(debug=True)
