#!/usr/bin/env python3
"""
Pinkberries flask-based web application.
"""
<<<<<<< HEAD
import certifi # resolve connection error for mongoDB
=======
>>>>>>> b7b0ca9232a87dd5d2a3e5d98c9c0196f5b3cf95
import os
import datetime
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values  ### You will need to install dotenv from terminal
from datetime import date
from flask import flash
from pymongo import MongoClient

load_dotenv()  # load environment variables from .env file

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 's3cr3t'
    # load flask config from env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where()) # resolve connection error for mongoDB
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)


    ### Add your functions here: ###
    @app.route("/")
    def home():
        try:
            # Fetch all exhibitions from the database without date filtering
            exhibitions = list(db.exhibitions.find())
            
            # Handle case where exhibitions might be None or empty
            if exhibitions is None:
                exhibitions = []
        
            #print("Exhibitions from the database:", exhibitions)
            # Pass the fetched exhibitions to the template
            return render_template("index.html", exhibitions=exhibitions)
        
        except Exception as e:
            print(f"Error occurred while fetching exhibitions: {e}")
        return f"An error occurred while fetching the exhibitions: {e}", 500

    @app.route("/exhibition/<exhibition_id>")
    def exhibition_detail(exhibition_id):
        exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
        
        if not exhibition:
            return "Exhibition not found", 404
        
        return render_template("exhibition_detail.html", exhibition=exhibition)

    @app.route("/create_exhibit", methods=["GET", "POST"])
    def create_exhibit():
        """
        Route for GET, POST requests to the create page.
        Accepts the form submission data for a new exhibit and saves the exhibition to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        if request.method == "POST":
            title = request.form["ftitle"]
            start = request.form["start_date"]
            end = request.form["end_date"]
            location = request.form["flocation"]
            cost = request.form["fcost"]
            artist = request.form["fartist"]
            artist_url = request.form["farturl"]
            art_style = request.form["fart_style"]
            art_medium = request.form["fart_medium"]
            event_type = request.form["fevent_type"]
            description = request.form["fdescription"]
            image_url = request.form["fimage_url"]
            created_by = request.form["created_by"]
<<<<<<< HEAD

            exhibition = {
                "title": title,
                "dates": {
                    "start": start,
                    "end": end
                },
                "location": location,
                "cost": cost,
                "artist": {
                    "artist": artist,
                    "profile_url": artist_url
                },
                "art_style": art_style,
                "art_medium": art_medium,
                "event_type": event_type,
                "description": description,
                "image_url": image_url,
                "created_by": created_by,
                "created_at": datetime.datetime.utcnow(),
            }
            
            # Insert into MongoDB
            db.exhibitions.insert_one(exhibition)
            # Redirect to the home page
            return redirect(url_for("home"))
        # If the method is GET, render the create exhibition form
        return render_template("create_exhibit.html")
    
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
        exhibition = db.exhibitions.find_one({"_id": ObjectId(post_id)})
        return render_template("edit.html", exhibition=exhibition)
    
    @app.route("/edit/<exhibition_id>", methods=["POST"])
    def edit_post(exhibition_id):
        """
        Route for POST requests to the edit page.
        Accepts the form submission data for the specified exhibit and updates the exhibit in the database.
        """
        # Get the existing exhibition from the database
        exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
        if not exhibition:
            return "Exhibition not found", 404

        # Initialize an empty dictionary to store updated fields
        updated_exhibition = {}

        # Get form data, only update if not empty
        title = request.form.get("ftitle")
        if title:
            updated_exhibition["title"] = title
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        if start or end:
            updated_exhibition["dates"] = {
                "start": start if start else exhibition["dates"]["start"],
                "end": end if end else exhibition["dates"]["end"]
            }
        location = request.form.get("flocation")
        if location:
            updated_exhibition["location"] = location
        cost = request.form.get("fcost")
        if cost:
            updated_exhibition["cost"] = cost
        artist = request.form.get("fartist")
        artist_url = request.form.get("farturl")
        if artist or artist_url:
            updated_exhibition["artist"] = {
                "artist": artist if artist else exhibition["artist"]["artist"],
                "profile_url": artist_url if artist_url else exhibition["artist"]["profile_url"]
            }
        art_style = request.form.get("fart_style")
        if art_style:
            updated_exhibition["art_style"] = art_style
        art_medium = request.form.get("fart_medium")
        if art_medium:
            updated_exhibition["art_medium"] = art_medium
        event_type = request.form.get("fevent_type")
        if event_type:
            updated_exhibition["event_type"] = event_type
        description = request.form.get("fdescription")
        if description:
            updated_exhibition["description"] = description
        image_url = request.form.get("fimage_url")
        if image_url:
            updated_exhibition["image_url"] = image_url
        created_by = request.form.get("created_by")
        if created_by:
            updated_exhibition["created_by"] = created_by

        # Always update the created_at field to the current timestamp when editing
        updated_exhibition["created_at"] = datetime.datetime.utcnow()

        # Only update the fields that were provided by the user
        if updated_exhibition:
            db.exhibitions.update_one({"_id": ObjectId(exhibition_id)}, {"$set": updated_exhibition})

        # Redirect to the exhibition detail page after the update
        return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))

    @app.route("/delete/<exhibition_id>", methods=["POST"])
    def delete(exhibition_id):
        try:
            object_id = ObjectId(exhibition_id)
            result = db.exhibitions.delete_one({"_id": object_id})
            
            if result.deleted_count == 0:
                flash('Exhibition not found or already deleted.', 'error')
                return redirect(url_for('home'))

            flash('Exhibition successfully deleted.', 'success')
            return redirect(url_for("home"))

        except Exception as e:
            flash(f"An error occurred while deleting the exhibition: {str(e)}", 'error')
            return redirect(url_for("home"))

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @app.route("/login")
    class GalleryOwner(UserMixin):
        def __init__(self, owner_id, username):
            self.id = str(owner_id)
            self.username = username
    
    @login_manager.user_loader
    def load_user(owner_id):
        owner_data = db.gallery_owners.find_one({"_id": ObjectId(owner_id)})
        if owner_data:
            return GalleryOwner(owner_data["_id"], owner_data["username"])
        else:
            return None

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            owner_data = db.gallery_owners.find_one({"username": username})

            if owner_data and owner_data["password"] == password:
                owner = GalleryOwner(owner_data["_id"], owner_data["username"])
                login_user(owner)  # Start session for the gallery owner
                flash("Login successful!", "success")
                return redirect(url_for("gallery_owner_page"))  # TEAMMATE NEED TO EDIT THIS!! THIS IS TEMPORRY
            else:
                flash("Gallery not found in database!", "error")

        return render_template("login.html")

    # TEAMMATE NEED TO EDIT THIS!! THIS IS TEMPORRY
    ###############################
    @app.route("/gallery_owner") 
    @login_required
    def gallery_owner_page():
        return f"Welcome, {current_user.username}! This is the Gallery Owner Dashboard."
=======
>>>>>>> b7b0ca9232a87dd5d2a3e5d98c9c0196f5b3cf95

            exhibition = {
                "title": title,
                "dates": {
                    "start": start,
                    "end": end
                },
                "location": location,
                "cost": cost,
                "artist": {
                    "artist": artist,
                    "profile_url": artist_url
                },
                "art_style": art_style,
                "art_medium": art_medium,
                "event_type": event_type,
                "description": description,
                "image_url": image_url,
                "created_by": created_by,
                "created_at": datetime.datetime.utcnow(),
            }
            
            # Insert into MongoDB
            db.exhibitions.insert_one(exhibition)
            # Redirect to the home page
            return redirect(url_for("home"))
        # If the method is GET, render the create exhibition form
        return render_template("create_exhibit.html")
    
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
        exhibition = db.exhibitions.find_one({"_id": ObjectId(post_id)})
        return render_template("edit.html", exhibition=exhibition)
    
    @app.route("/edit/<exhibition_id>", methods=["POST"])
    def edit_post(exhibition_id):
        """
        Route for POST requests to the edit page.
        Accepts the form submission data for the specified exhibit and updates the exhibit in the database.
        """
        # Get the existing exhibition from the database
        exhibition = db.exhibitions.find_one({"_id": ObjectId(exhibition_id)})
        if not exhibition:
            return "Exhibition not found", 404

<<<<<<< HEAD
=======
        # Initialize an empty dictionary to store updated fields
        updated_exhibition = {}

        # Get form data, only update if not empty
        title = request.form.get("ftitle")
        if title:
            updated_exhibition["title"] = title
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        if start or end:
            updated_exhibition["dates"] = {
                "start": start if start else exhibition["dates"]["start"],
                "end": end if end else exhibition["dates"]["end"]
            }
        location = request.form.get("flocation")
        if location:
            updated_exhibition["location"] = location
        cost = request.form.get("fcost")
        if cost:
            updated_exhibition["cost"] = cost
        artist = request.form.get("fartist")
        artist_url = request.form.get("farturl")
        if artist or artist_url:
            updated_exhibition["artist"] = {
                "artist": artist if artist else exhibition["artist"]["artist"],
                "profile_url": artist_url if artist_url else exhibition["artist"]["profile_url"]
            }
        art_style = request.form.get("fart_style")
        if art_style:
            updated_exhibition["art_style"] = art_style
        art_medium = request.form.get("fart_medium")
        if art_medium:
            updated_exhibition["art_medium"] = art_medium
        event_type = request.form.get("fevent_type")
        if event_type:
            updated_exhibition["event_type"] = event_type
        description = request.form.get("fdescription")
        if description:
            updated_exhibition["description"] = description
        image_url = request.form.get("fimage_url")
        if image_url:
            updated_exhibition["image_url"] = image_url
        created_by = request.form.get("created_by")
        if created_by:
            updated_exhibition["created_by"] = created_by

        # Always update the created_at field to the current timestamp when editing
        updated_exhibition["created_at"] = datetime.datetime.utcnow()

        # Only update the fields that were provided by the user
        if updated_exhibition:
            db.exhibitions.update_one({"_id": ObjectId(exhibition_id)}, {"$set": updated_exhibition})

        # Redirect to the exhibition detail page after the update
        return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))

    @app.route("/delete/<exhibition_id>", methods=["POST"])
    def delete(exhibition_id):
        try:
            object_id = ObjectId(exhibition_id)
            result = db.exhibitions.delete_one({"_id": object_id})
            
            if result.deleted_count == 0:
                flash('Exhibition not found or already deleted.', 'error')
                return redirect(url_for('home'))

            flash('Exhibition successfully deleted.', 'success')
            return redirect(url_for("home"))

        except Exception as e:
            flash(f"An error occurred while deleting the exhibition: {str(e)}", 'error')
            return redirect(url_for("home"))
>>>>>>> b7b0ca9232a87dd5d2a3e5d98c9c0196f5b3cf95
    return app

### Here is where the app gets created: ###
app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
