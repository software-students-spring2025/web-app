from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, g
from dotenv import load_dotenv
import flask_login
import os
import pymongo
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

def create_app():
    app = Flask(__name__)

    load_dotenv()
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

    print(MONGO_URI)

    #make a connection to the database server
    connection = pymongo.MongoClient(MONGO_URI)
    db = connection["Jitter"]
    users = db.user
    #g._database = db

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)    

    return app
