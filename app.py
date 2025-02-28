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
        
        today = date.today()
        today = today.strftime("%Y-%m-%d")

        exhibitions = list(db.exhibitions.find({"dates.end": {"$gte": today}}))
        print("Exhibitions matching query:", exhibitions)
    
        return render_template("index.html", exhibitions=exhibitions)

    @app.route("/exhibition/<exhibition_id>")
    def exhibition_detail(exhibition_id):
        exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
        
        if not exhibition:
            return "Exhibition not found", 404
        
        return render_template("exhibition_detail.html", exhibition=exhibition)

    @app.route("/create_exhibit", methods=["POST"])
    def create_exhibit():
        """
        Route for POST requests to the create page.
        Accepts the form submission data for a new exhibit and saves the exhibition to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        title = request.form["ftitle"]
        dates = request.form["fdates"]
        location = request.form["flocation"]
        cost = request.form["fcost"]
        artist = request.form["fartist"]
        art_style = request.form["fart_style"]
        art_medium = request.form["fart_medium"]
        event_type = request.form["fevent_type"]
        description = request.form["fdescription"]
        image_url = request.form["fimage_url"]
        created_by = request.form["created_by"]
        exhibition = {
            "Exhibition Title": title,
            "Dates": dates,
            "Location": location,
            "Cost": cost,
            "Artist": artist,
            "Art Style": art_style,
            "Art Medium": art_medium,
            "Event Type": event_type,
            "Description" : description,
            "Image_url" : image_url,
            "Created_by" : created_by,
            "created_at": datetime.datetime.utcnow(),
        }
        db.exhibits.insert_one(exhibition)

        return redirect(url_for("home"))
    
    @app.route("/edit/<post_id>")
    def edit(post_id):
        """
        Route for GET requests to the edit page.
        Displays a form users can fill out to edit an existing record.
        Args:
            post_id (str): The ID of the post to edit.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        exhibition = db.exhibits.find_one({"_id": ObjectId(post_id)})
        return render_template("edit.html", exhibition=exhibition)

    @app.route("/edit/<post_id>", methods=["POST"])
    def edit_post(post_id):
        """
        Route for POST requests to the edit page.
        Accepts the form submission data for the specified exhibit and updates the exhibit in the database.
        Args:
            post_id (str): The ID of the post to edit.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        title = request.form["ftitle"]
        dates = request.form["fdates"]
        location = request.form["flocation"]
        cost = request.form["fcost"]
        artist = request.form["fartist"]
        art_style = request.form["fart_style"]
        art_medium = request.form["fart_medium"]
        event_type = request.form["fevent_type"]
        description = request.form["fdescription"]
        image_url = request.form["fimage_url"]
        created_by = request.form["created_by"]

        exhibition = {
            "Exhibition Title": title,
            "Dates": dates,
            "Location": location,
            "Cost": cost,
            "Artist": artist,
            "Art Style": art_style,
            "Art Medium": art_medium,
            "Event Type": event_type,
            "Description" : description,
            "Image url" : image_url,
            "Created by" : created_by,
            "Created at": datetime.datetime.utcnow(),
        }

        db.exhibition.update_one({"_id": ObjectId(post_id)}, {"$set": exhibition})

        return redirect(url_for("home"))

    @app.route("/delete/<post_id>")
    def delete(post_id):
        """
        Route for GET requests to the delete page.
        Deletes the specified record from the database, and then redirects the browser to the home page.
        Args:
            post_id (str): The ID of the post to delete.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        db.messages.delete_one({"_id": ObjectId(post_id)})
        return redirect(url_for("home"))

    @app.route("/delete-by-content/<Created_by>/<Exhibition_title>", methods=["POST"])
    def delete_by_content(Created_by, Exhibition_title):
        """
        Route for POST requests to delete exhibition by their creator's name and exhibit title.
        Deletes the specified record from the database, and then redirects the browser to the home page.
        Args:
            Created_by (str): The name of the creator of the exhibit.
            Exhibition_title (str): The title of the exhibition to be deleted.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        db.exhibits.delete_many({"Created by": Created_by, "Exhibition Title": Exhibition_title})
        return redirect(url_for("home"))

### Here is where the app gets created: ###
app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
