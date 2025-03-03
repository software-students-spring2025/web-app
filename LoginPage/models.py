from flask_login import UserMixin
from app import mongo

#class to set user information
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # MongoDB _id is an ObjectId, convert to string
        self.username = user_data['username']
        self.password = user_data['password']

    #can only be called inside the class: gets user info 
    @staticmethod
    def get_user(username):
        """Fetch a user from MongoDB"""
        user_data = mongo.db.users.find_one({"username": username})
        return User(user_data) if user_data else None
