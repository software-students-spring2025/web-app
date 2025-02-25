import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
import pymongo
from dotenv import load_dotenv, dotenv_values
from bson.objectid import ObjectId
from datetime import datetime

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


# A simple user model that wraps a MongoDB document.
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])  # Flask-Login expects a string ID.
        self.username = user_data["username"]
        self.password_hash = user_data["password"]


def create_app():
    app = Flask(__name__)
    config = dotenv_values()
    app.config.from_mapping(config)
    # Ensure you have a secret key for session management.
    app.secret_key = os.getenv("SECRET_KEY", "defaultsecretkey")

    # Set up MongoDB connection.
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" * Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    # Set up Flask-Login.
    login_manager = LoginManager()
    login_manager.login_view = "login_form"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    # --- Routes for Todos ---

    @app.route("/todos/new", methods=["GET"])
    @login_required
    def add_todo_form():
        return render_template("add_todo.html")

    @app.route("/todos/<id>/edit", methods=["GET"])
    @login_required
    def edit_todo_form(id):
        todo = db.todos.find_one({"_id": ObjectId(id), "user_id": current_user.id})
        if not todo:
            return "Todo not found or unauthorized", 404
        return render_template("edit_todo.html", todo=todo)

    # Home now requires login and only shows the current user's todos.
    @app.route("/")
    @login_required
    def home():
        todos = list(db.todos.find({"user_id": current_user.id}).sort("created_at", -1))
        for todo in todos:
            todo["_id_str"] = str(todo["_id"])
        return render_template("index.html", todos=todos)

    @app.route("/todos", methods=["GET"])
    @login_required
    def get_todos():
        q = request.args.get("q")
        # Always filter by the current user.
        base_query = {"user_id": current_user.id}
        if q:
            query = {
                "$and": [
                    base_query,
                    {
                        "$or": [
                            {"name": {"$regex": q, "$options": "i"}},
                            {"message": {"$regex": q, "$options": "i"}},
                        ]
                    },
                ]
            }
        else:
            query = base_query
        todos = list(db.todos.find(query).sort("created_at", -1))
        return render_template("index.html", todos=todos)

    @app.route("/todos/<id>", methods=["GET"])
    @login_required
    def get_todo(id):
        try:
            todo = db.todos.find_one({"_id": ObjectId(id), "user_id": current_user.id})
            if not todo:
                return "Todo not found or unauthorized", 404
            return render_template("detail.html", todo=todo)
        except Exception as e:
            return str(e), 400

    @app.route("/todos", methods=["POST"])
    @login_required
    def create_todo():
        name = request.form.get("fname")
        message = request.form.get("fmessage")
        if not name or not message:
            return "Missing name or message", 400
        todo = {
            "name": name,
            "message": message,
            "created_at": datetime.utcnow(),
            "user_id": current_user.id,  # Associate with the logged in user.
        }
        db.todos.insert_one(todo)
        return redirect(url_for("home"))

    @app.route("/todos/<id>", methods=["POST"])
    @login_required
    def edit_todo(id):
        name = request.form.get("fname")
        message = request.form.get("fmessage")
        if not name or not message:
            return "Missing name or message", 400
        # Ensure the todo belongs to the current user.
        todo = db.todos.find_one({"_id": ObjectId(id)})
        if not todo or todo.get("user_id") != current_user.id:
            return "Todo not found or unauthorized", 404
        try:
            result = db.todos.update_one(
                {"_id": ObjectId(id), "user_id": current_user.id},
                {
                    "$set": {
                        "name": name,
                        "message": message,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
            if result.matched_count == 0:
                return "Todo not found", 404
            return redirect(url_for("home"))
        except Exception as e:
            return str(e), 400

    @app.route("/todos/<id>/delete", methods=["POST"])
    @login_required
    def delete_todo(id):
        # Check authorization before deleting.
        todo = db.todos.find_one({"_id": ObjectId(id)})
        if not todo or todo.get("user_id") != current_user.id:
            return "Todo not found or unauthorized", 404
        try:
            result = db.todos.delete_one(
                {"_id": ObjectId(id), "user_id": current_user.id}
            )
            if result.deleted_count == 0:
                return "Todo not found", 404
            return redirect(url_for("home"))
        except Exception as e:
            return str(e), 400

    # --- Authentication Routes ---

    @app.route("/login", methods=["GET"])
    def login_form():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = db.users.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login_form"))

    @app.route("/signup", methods=["POST"])
    def signup():
        username = request.form.get("username")
        password = request.form.get("password")
        if db.users.find_one({"username": username}):
            flash("Username already exists.")
            return redirect(url_for("login_form"))
        password_hash = generate_password_hash(password)
        user_data = {"username": username, "password": password_hash}
        result = db.users.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        user = User(user_data)
        login_user(user)
        flash("Signup successful. You are now logged in.")
        return redirect(url_for("home"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.")
        return redirect(url_for("login_form"))

    @app.errorhandler(Exception)
    def handle_error(e):
        return render_template("error.html", error=e)

    return app


app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")
    app.run(port=int(FLASK_PORT))
