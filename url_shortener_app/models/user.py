from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User(UserMixin):
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": user_id})

    @staticmethod
    def create_user(username, password):
        if User.find_by_username(username):
            return None
        password_hash = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({"username": username, "password_hash": password_hash}).inserted_id
        return User(user_id, username, password_hash)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
