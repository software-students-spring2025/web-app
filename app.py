from flask import Flask, request, jsonify, session, render_template, redirect, url_for, abort
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
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
    return jsonify({"status": "success", "message": "API is running"})

# Route to serve HTML templates
@app.route('/', defaults={'page_name': 'index'})
@app.route('/<page_name>')
def serve_page(page_name):
    """
    Serve HTML templates based on the page name
    This allows for dynamic routing to any template
    """
    # List of valid pages (add more as needed) #TODO: Add more pages
    valid_pages = [
        'index', 'login', 'register', 'profile', 'preferences',
        'matches', 'messages', 'notifications', 'bookmarks'
    ]
    
    # Check if the requested page exists
    if page_name not in valid_pages:
        abort(404)
    
    try:
        # Set active page for navigation highlighting
        return render_template(f'{page_name}.html', active_page=page_name)
    except:
        # If template doesn't exist, return 404
        abort(404)

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    # TODO: Implement user registration
    return jsonify({"status": "success", "message": "Registration endpoint"})

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login a user"""
    # TODO: Implement user login
    return jsonify({"status": "success", "message": "Login endpoint"})

@app.route('/api/auth/logout')
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

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
    user_id = current_user.id
    result = db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0: 
        return jsonify({"status": "error", "message": "User not found"}), 404
    logout_user()

    return jsonify({"status": "success", "message": "Account deleted successfully"})
    

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
    if not ObjectId.is_valid(notification_id): 
        return jsonify({"status": "error", "message": "Invalid notification ID"}), 400
    
    result = db.notifications.update_one(
        {"_id": ObjectId(notification_id), "user_id": ObjectId(current_user.id)}, 
        {"$set": {"read": True}}
    )
    if result.matched_count == 0: 
        return jsonify({"status": "error", "message": "Notification not found"}), 404
    return jsonify({"status": "success", "message": "Notification marked as read"}), 200


if __name__ == '__main__':
    app.run(debug=True) 