from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import json
from bson import ObjectId
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

# Custom JSON encoder to handle MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

# Initialize Flask app
app = Flask(__name__)
app.json_encoder = JSONEncoder
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Enable CORS
CORS(app)

# Configure MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client.travel_match_db

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # TODO: Implement user loading from MongoDB
    pass

# Routes
@app.route('/api/hello_world', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({"status": "ok", "message": "Hello World"}), 200

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    # TODO: Implement user registration
    # - Get username, email, password from request
    # - Check if user already exists
    # - Hash password
    # - Store user in database
    # - Return success/error response
    pass

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login a user"""
    # TODO: Implement user login
    # - Get username/email and password from request
    # - Check if user exists
    # - Verify password
    # - Login user with Flask-Login
    # - Return user data
    pass

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user"""
    # TODO: Implement user logout
    # - Logout user with Flask-Login
    # - Return success response
    pass

# User Profile Routes
@app.route('/api/users/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get current user's profile"""
    # TODO: Implement fetching user profile
    # - Get user from current_user
    # - Return user profile data
    pass

@app.route('/api/users/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """Update current user's profile"""
    # TODO: Implement updating user profile
    # - Get profile data from request
    # - Update user in database
    # - Return updated user data
    pass

@app.route('/api/users/profile', methods=['DELETE'])
@login_required
def delete_user_profile():
    """Delete current user's account"""
    # TODO: Implement deleting user account
    # - Remove user from database
    # - Logout user
    # - Return success response
    pass

# Travel Preferences Routes
@app.route('/api/preferences', methods=['GET'])
@login_required
def get_preferences():
    """Get current user's travel preferences"""
    # TODO: Implement fetching travel preferences
    # - Get preferences from database
    # - Return preferences data
    pass

@app.route('/api/preferences', methods=['POST'])
@login_required
def create_preferences():
    """Create travel preferences for current user"""
    # TODO: Implement creating travel preferences
    # - Get preference data from request
    # - Store preferences in database
    # - Return created preferences
    pass

@app.route('/api/preferences', methods=['PUT'])
@login_required
def update_preferences():
    """Update current user's travel preferences"""
    # TODO: Implement updating travel preferences
    # - Get preference data from request
    # - Update preferences in database
    # - Return updated preferences
    pass

# Travel Partner Matching Routes
@app.route('/api/matches', methods=['GET'])
@login_required
def get_matches():
    """Get travel partner matches for current user"""
    # TODO: Implement fetching matches
    # - Get user preferences
    # - Find matching users based on preferences
    # - Return matches
    pass

@app.route('/api/matches/search', methods=['POST'])
@login_required
def search_matches():
    """Search for travel partners based on specific criteria"""
    # TODO: Implement searching for matches
    # - Get search criteria from request
    # - Find matching users based on criteria
    # - Return matches
    pass

# Bookmarking Routes
@app.route('/api/bookmarks', methods=['GET'])
@login_required
def get_bookmarks():
    """Get current user's bookmarked profiles"""
    # TODO: Implement fetching bookmarks
    # - Get bookmarks from database
    # - Return bookmarked profiles
    pass

@app.route('/api/bookmarks/<user_id>', methods=['POST'])
@login_required
def add_bookmark(user_id):
    """Bookmark a user profile"""
    # TODO: Implement adding bookmark
    # - Validate target user_id
    # - Add bookmark to database
    # - Return success response
    pass

@app.route('/api/bookmarks/<user_id>', methods=['DELETE'])
@login_required
def remove_bookmark(user_id):
    """Remove a bookmarked profile"""
    # TODO: Implement removing bookmark
    # - Validate target user_id
    # - Remove bookmark from database
    # - Return success response
    pass

# Messaging Routes
@app.route('/api/messages', methods=['GET'])
@login_required
def get_conversations():
    """Get all conversations for current user"""
    # TODO: Implement fetching conversations
    # - Get conversations from database
    # - Return conversations data
    pass

@app.route('/api/messages/<user_id>', methods=['GET'])
@login_required
def get_messages(user_id):
    """Get messages between current user and another user"""
    # TODO: Implement fetching messages
    # - Validate target user_id
    # - Get messages from database
    # - Return messages data
    pass

@app.route('/api/messages/<user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    """Send a message to another user"""
    # TODO: Implement sending message
    # - Validate target user_id
    # - Get message content from request
    # - Store message in database
    # - Return success response
    pass

# Notification Routes
@app.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for current user"""
    # TODO: Implement fetching notifications
    # - Get notifications from database
    # - Return notifications data
    pass

@app.route('/api/notifications/<notification_id>', methods=['PUT'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    # TODO: Implement marking notification as read
    # - Validate notification_id
    # - Update notification in database
    # - Return success response
    pass

if __name__ == '__main__':
    app.run(debug=True) 