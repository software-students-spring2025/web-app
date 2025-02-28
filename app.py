#!/usr/bin/env python3

"""
Pinkberries flask-based web application.
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values  ### You will need to install dotenv from terminal
from datetime import date

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

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)




    ### Add your functions here: ###
    @app.route("/")
    def home():
        # Fetch upcoming exhibitions (filter out past ones)\
        
        today = date.today()
        today = today.strftime("%Y-%m-%d")

        exhibitions = list(db.exhibitions.find({"dates.end": {"$gte": today}}))
        print("Exhibitions matching query:", exhibitions)
    
        return render_template("index.html", exhibitions=exhibitions)
        # exhibitions = [
        #     {
        #         "title": "Test Exhibition",
        #         "dates": {"start": "2025-03-15", "end": "2025-04-30"},
        #         "location": "ArtSpace Gallery",
        #         "cost": 10.0,
        #         "artist": {"name": "Test Artist"},
        #         "art_style": "Impressionist",
        #         "art_medium": "Paintings",
        #         "event_type": "Launch Party",
        #         "description": "An exhibition for testing.",
        #         "image_url": "",
        #     }
        # ]
        #return render_template("index.html", exhibitions=exhibitions)





    @app.route("/create", methods=["POST"])
    def create_post():
        # Handle post creation logic here
        return redirect(url_for('home'))  # Example redirect after handling POST
    
    @app.route("/test-mongo")
    def test_mongo():
        try:
            # Example: Insert a document into a test collection
            result = db.test_collection.insert_one({"name": "Pinkberry", "flavor": "Strawberry"})
            # Retrieve the document
            test_data = db.test_collection.find_one({"_id": result.inserted_id})
            return f"MongoDB Test Successful! Data inserted: {test_data}"
        except Exception as e:
            return f"Error: {e}"

    return app  # Make sure to return the app instance

### Here is where the app gets created: ###
app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
