import pymongo
from flask import request, current_app, g
import bson
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from .dbconnect import get_db

def insert_data():
    print("in insert data")
    if request.method == 'POST':
        db = get_db()
        print("request method post")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        reg_user = {}
        reg_user['name'] = name
        reg_user['email'] = email
        reg_user['password'] = password

        users = db['user']
        if users.find_one({"email":email}) == None:
            users.insert_one(reg_user)
            return True
        else:
            return False


def check_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = {
            "email": email,
            "password": password
        }

        user_data = users.find_one(user)
        if user_data == None:
            return False, ""
        else:
            return True, user_data["name"]
