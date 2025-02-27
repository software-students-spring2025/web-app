from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Secret key for session security
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# MongoDB Configuration (Using PyMongo Instead of Flask-MongoEngine)
app.config['MONGO_URI'] = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORT', '27017')}/{os.getenv('MONGO_DB', 'project2')}"

# Initialize PyMongo
mongo = PyMongo(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model (Manual Handling Instead of Flask-MongoEngine)
class User(UserMixin):
    def __init__(self, username, email, password_hash, _id=None):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": user_id})
    if not user_data:
        return None
    return User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])

# Home Route
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username already exists
        if mongo.db.users.find_one({"username": username}):
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        user = User(username, email, None)
        user.set_password(password)
        mongo.db.users.insert_one({
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash
        })
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = mongo.db.users.find_one({"username": username})

        if user_data:
            user = User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Dashboard Route (Protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! Welcome to your dashboard.'

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
