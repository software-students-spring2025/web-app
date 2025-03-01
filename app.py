#!/usr/bin/env python3

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # Load environment variables

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
config = dotenv_values()
app.config.from_mapping(config)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

# Initialize Flask-Login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User model for authentication
class User(flask_login.UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])  # Ensure ID is a string for Flask-Login compatibility
        self.email = user_data["email"]
        self.username = user_data["username"]
        self.password = user_data["password"]

    @staticmethod
    def find_by_username(username):
        """Find user by username in MongoDB."""
        user_data = db.loginInfo.find_one({"username": username})
        return User(user_data) if user_data else None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID in MongoDB."""
        user_data = db.loginInfo.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None

    @staticmethod
    def create_user(email, username, password):
        """Create a new user in MongoDB."""
        if db.loginInfo.find_one({"username": username}):
            return False  # Username already exists
        
        if db.loginInfo.find_one({"email": email}):
            return False  # Email already exists
        
        hashed_password = generate_password_hash(password) 
        db.loginInfo.insert_one({
            "email": email,
            "username": username,
            "password": hashed_password
        })
        return True


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


    @app.route("/")
    def index():
        return redirect(url_for("login"))

    #loginpage
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        
        elif request.method == "POST":
            #add log in logic
            return render_template("login.html", test="data to send in")

    #registerpage
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        
        elif request.method == "POST":
            #add log in logic
            return render_template("register.html", test="data to send in")

    return app

app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=int(FLASK_PORT), debug=(FLASK_ENV == "development"))