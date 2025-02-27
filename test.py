"""
Flask-based web app.
"""
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values  # You will need to install dotenv from terminal first

# Load environment variables from the .env file
load_dotenv()

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """
    app = Flask(__name__)
    # load flask config from env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    # Ensure the MONGO_DBNAME environment variable is correctly set
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" * Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)


    @app.route("/")
    def home():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        docs = db.exhibits.find({}).sort("creatd_at", -1)
        return render_template("index.html", docs=docs)


    @app.route("/create_exhibit", methods=["POST"])
    def create_exhibit():
        """
        Route for POST requests to the create page.
        Accepts the form submission data for a new exhibit and saves the exhibition to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        name = request.form["fname"]
        description = request.form["fdescription"]
        artist = request.form["fartist"]
        time_frame = request.form["ftime_frame"]
        location = request.form["flocation"]
        date = request.form["fdate"]
        cost = request.form["cost"]

        exhibition = {
            "Exhibition Name": name, 
            "Description": description,
            "Artists": artist,
            "Time Period": time_frame,
            "Location": location,
            "Exhibit Dates": date,
            "Cost": cost,
            "created_at": datetime.datetime.utcnow(),
        }
        db.exhibits.insert_one(exhibition)
        return redirect(url_for("home"))

#app = create_app()
if __name__ == "__main__":
    #FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    #FLASK_ENV = os.getenv("FLASK_ENV")
    #print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(debug=True)
