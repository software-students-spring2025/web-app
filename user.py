import os
import pymongo 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv, dotenv_values

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]  

user_bp = Blueprint("user", __name__)

login_manager = LoginManager()
login_manager.login_view = "user.login"

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"]) 
        self.username = user_data["username"]
        self.password_hash = user_data["password"]

    @staticmethod
    def find_by_username(username):
        """Fetch user by username from MongoDB"""
        users_collection = db.loginInfo         
        user_data = users_collection.find_one({"username": username})
        return User(user_data) if user_data else None

    @staticmethod
    def find_by_id(user_id):
        """Fetch user by ID from MongoDB"""
        users_collection = db.loginInfo  
        user_data = users_collection.find_one({"_id": user_id})
        return User(user_data) if user_data else None

    @staticmethod
    def create_user(username, password):
        """Insert a new user into MongoDB with hashed password"""
        users_collection = db.loginInfo  

        if users_collection.find_one({"username": username}):
            return False 
        
        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        return True

    def check_password(self, password):
        """Check if password matches stored hash"""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    users_collection = db.loginInfo  
    return users_collection.find_by_username(user_id)

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        users_collection = db.loginInfo 
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("user.register"))

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful, please login.", "success")
        return redirect(url_for("user.login"))

    return render_template("register.html")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.find_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))  # Change to your main page

        flash("Invalid credentials", "danger")
    
    return render_template("login.html")

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("user.login"))