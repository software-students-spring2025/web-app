from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register Blueprints
from routes.auth import auth
from routes.urls import urls

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(urls, url_prefix="/urls")

if __name__ == "__main__":
    app.run(debug=True)
