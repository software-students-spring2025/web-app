import pymongo
from flask import request, current_app, g
import bson
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    mydb = getattr(g, "_database", None)

    if mydb is None:
        mydb = g._database = PyMongo(current_app).db
    return mydb

def insert_data():
    print("in insert data")
    if request.method == 'POST':
        print("request method post")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)  # Hash password

        reg_user = {
            "name": name,
            "email": email,
            "password": hashed_password  # Store hashed password
        }

        db = get_db()
        users = db.user

        if users.find_one({"email": email}) is None:
            users.insert_one(reg_user)
            return True
        else:
            return False

def check_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        users = db.user

        user_data = users.find_one({"email": email})

        if user_data is None:
            return False, ""
        else:
            # Check hashed password
            if check_password_hash(user_data["password"], password):
                return True, user_data["name"]
            else:
                return False, ""
