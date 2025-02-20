from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from models.user import User

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")


# Fallback in case the key is missing
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application. Set it in your .env file!")

# Initialize MongoDB
mongo = PyMongo(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    user_data = User.find_by_id(user_id)
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password_hash"])
    return None

# Register blueprints properly
def register_blueprints():
    from routes.auth import auth
    from routes.urls import urls
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(urls, url_prefix="/urls")

register_blueprints()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
