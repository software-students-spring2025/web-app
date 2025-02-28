from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config 

app = Flask(__name__) 

app.config.from_object(Config) 

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect if not logged in 


# Import routes
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
