from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from bson.objectid import ObjectId
from app import mongo

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, role="user"):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(id=user_data["_id"], **user_data)
        return None

    @staticmethod
    def create(username, email, password, role="user"):
        password_hash = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": role
        }).inserted_id
        return str(user_id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

class Post:
    @staticmethod
    def create(game_name, level, platform, description, availability, region, created_by, contact):
        post_id = mongo.db.posts.insert_one({
            "game_name": game_name,
            "level": level,
            "platform": platform,
            "description": description,
            "availability": availability,
            "region": region,
            "created_by": ObjectId(created_by),
            "contact": contact,
            "created_at": datetime.utcnow()
        }).inserted_id
        return str(post_id)

    @staticmethod
    def find_all():
        return list(mongo.db.posts.find())

    @staticmethod
    def find_by_id(post_id):
        return mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    @staticmethod
    def delete(post_id):
        mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
