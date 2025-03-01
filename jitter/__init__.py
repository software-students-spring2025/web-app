from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
import flask_login
import os
import pymongo
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    load_dotenv()
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

    print(MONGO_URI)
    # make a connection to the database server
    connection = pymongo.MongoClient(MONGO_URI)
    db = connection["Jitter"]

    doc = {
    "name": "Foo Barstein",
    "email": "fb1258@nyu.edu",
    "message": "We loved with a love that was more than love.\n -Edgar Allen Poe",
    "created_at": datetime.datetime.utcnow() # the date time now
    }

    mongoid = db.collection_name.insert_one(doc)

    return app
'''
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
'''
    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
'''

