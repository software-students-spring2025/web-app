#!/usr/bin/env python3

"""
Example flask-based web application.
See the README.md file for instructions how to set up and run the app in development mode.
"""

import os
import datetime
import flask_login
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """

    app = Flask(__name__)
    # load flask config from env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.login_view="login"

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    return app, db, login_manager

app, db, login_manager = create_app()

@login_manager.user_loader
def user_loader(id):
    user_data = db.loginInfo.find_one({"_id":ObjectId(id)})
    if user_data:
        return User(str(user_data['_id']),user_data['email'],user_data['password'])
    return None

@app.route("/")
def index():
    return redirect("/register")
    
#registerpage
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        exist = mongo.db.loginInfo.find_one({"email":request.form['email']})
        if exist is None:
            doc={
                'email':request.form['email'],
                'username':request.form['username'],
                'password':request.form['password']
            }
            db.loginInfo.insert_one(doc)
            return redirect("/login")
        else:
            #error message here, this email has already been used
            return redirect("/register")
       
#loginpage
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        user = users.get(request.form["email"])
        if user is None or user.password!=request.form["password"]:
            return redirect("/login")
        flask_login.login_user
        return redirect("/home")

@app.route("/home")
@flask_login.login_required
def home():
    return render_remplate('home.html')

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/login")

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
