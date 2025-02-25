#!/usr/bin/env python3

# Citation: Flask app example


#This is a super basic template for our flask that we can fill out

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

def create_app():
    # Create and config the Flask app, static folder is for files and images we want to have (I also added a static folder)
    app = Flask(__name__, static_folder='static')
    
    # Load flask config from env
    load_dotenv()
    config = dotenv_values()
    app.config.from_mapping(config)
    
    # Connect to MongoDB
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]
    
    # Check connection
    cxn.admin.command("ping")
    print(" *", "Connected to MongoDB!")
    
    # Homepage
    @app.route("/")
    def home():
        return render_template("index.html")
    
    # Other page
    @app.route("/page1")
    def page1():
        return render_template("page.html", title = 'page', paragraph_text = 'some text')
    
    # Admin or owner page
    @app.route("/admin")
    def edit():
        return render_template("owner.html")
    
    # Error page
    @app.errorhandler(Exception)
    def handle_error(e):
        return render_template("errorpage.html")
    
    return app


if __name__ == "__main__":
    app = create_app()
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")
    app.run(port=int(FLASK_PORT))