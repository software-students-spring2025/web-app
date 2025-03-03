import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    UserMixin,
    current_user,
)
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "yoursecretkey"

# Set up MongoDB connection using pymongo
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.get_database("jobtracker")
users_collection = db.get_collection("users")
applications_collection = db.get_collection("applications")

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Define a User class that integrates with Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = users_collection.find_one({"email": email})

        if user_data and check_password_hash(user_data["password"], password):
            user_obj = User(user_data)
            login_user(user_obj)
            flash("Logged in successfully", "success")
            return redirect(url_for("home"))  # Redirect clears the flash message

        else:
            flash("Invalid email or password", "danger")
    
    return render_template("login.html")  # Flash messages only shown after submission


# Route for user signup (for creating new accounts)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("signup"))
        # Check if the user already exists
        if users_collection.find_one({"email": email}):
            flash("Email already registered", "danger")
            return redirect(url_for("signup"))
        # Hash the password and store the user data
        hashed_password = generate_password_hash(password)
        user_id = users_collection.insert_one(
            {"email": email, "password": hashed_password}
        ).inserted_id
        user_data = users_collection.find_one({"_id": user_id})
        user_obj = User(user_data)
        login_user(user_obj)
        flash("Account created and logged in", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")

# Home screen (protected route)
@app.route("/home", methods=["GET"])
@login_required
def home():
    search_query = request.args.get("search", "").strip()

    if search_query:
        applications = list(applications_collection.find({
            "$and": [
                {"user_id": current_user.id},
                {"$or": [
                    {"company": {"$regex": search_query, "$options": "i"}},
                    {"job_title": {"$regex": search_query, "$options": "i"}}
                ]}
            ]
        }))
    else:
        applications = list(applications_collection.find({"user_id": current_user.id}))

    total_apps = len(applications)
    interview_count = sum(1 for app in applications if app.get("status") == "Interview")
    offer_count = sum(1 for app in applications if app.get("status") == "Offered")

    return render_template(
        "home.html",
        applications=applications,
        user=current_user,
        total_apps=total_apps,
        interview_count=interview_count,
        offer_count=offer_count
    )

@app.route("/add_application", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        applications_collection.insert_one({
            "user_id": current_user.id,
            "company": company,
            "job_title": job_title,
            "status": status,
            "application_date": application_date,
            "note": note
        })

        flash("New application added!", "success")
        return redirect(url_for("home"))

    return render_template("add_application.html")

# Route for logging out the user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))

@app.route("/delete_application/<application_id>", methods=["GET"])
@login_required
def delete_application(application_id):
    applications_collection.delete_one({"_id": ObjectId(application_id)})
    flash("Application deleted successfully!", "success")
    return redirect(url_for("home"))

@app.route("/edit_application/<application_id>", methods=["GET", "POST"])
@login_required
def edit_application(application_id):
    application = applications_collection.find_one({"_id": ObjectId(application_id)})

    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        applications_collection.update_one(
            {"_id": ObjectId(application_id)},
            {"$set": {
                "company": company,
                "job_title": job_title,
                "status": status,
                "application_date": application_date,
                "note": note
            }}
        )
        flash("Application updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_application.html", application=application)
@app.route("/search_application", methods=["GET", "POST"])
@login_required
def search_application():
    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        # Build search query
        query = {"user_id": current_user.id}
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        if job_title:
            query["job_title"] = {"$regex": job_title, "$options": "i"}
        if status:
            query["status"] = {"$regex": status, "$options": "i"}
        if application_date:
            query["application_date"] = application_date
        if note:
            query["note"] = {"$regex": note, "$options": "i"}

        # Perform search in MongoDB
        search_results = list(applications_collection.find(query))

        return render_template("search_results.html", results=search_results)

    return render_template("search_application.html")


if __name__ == "__main__":
    app.run(debug=True)
