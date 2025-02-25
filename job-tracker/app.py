#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
import certifi
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file


def create_app():
    app = Flask(__name__)

    config = dotenv_values()
    app.config.from_mapping(config)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"),
                              tlsCAFile=certifi.where())
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    # ObjectId of current logged in user. Will have to fetch this with pymongo commands later
    loggedUser = ObjectId('67bd0feb736f2e7829d2dbe9')

    # landing page
    @app.route('/')
    def landing():
        return render_template("landing.html")

    # login page
    @app.route('/login')
    def login():
        return render_template("login.html")

    # signup page
    @app.route('/signup')
    def signup():
        return render_template("signup.html")

    # home page
    @app.route('/home')
    def home():
        # finding total apps of user
        total = db.Apps.count_documents({"user": loggedUser})

        # calculating dates
        today = datetime.now()

        week = today - timedelta(days=today.weekday())
        month = datetime(today.year, today.month, 1)

        iso_week = week.replace(hour=0, minute=0, second=0, microsecond=0)
        iso_month = month.replace(hour=0, minute=0, second=0, microsecond=0)

        # documents created this week and month
        docs_week_cursor = db.Apps.find({
            "date": {
                "$gte": iso_week
            },
            "user": loggedUser
        })
        docs_month_cursor = db.Apps.find({
            "date": {
                "$gte": iso_month
            },
            "user": loggedUser
        })

        # convert to lists
        docs_week = list(docs_week_cursor)
        docs_month = list(docs_month_cursor)

        # finding number of apps based on status
        accepted = db.Apps.count_documents({
            "status": "Accepted",
            "user": loggedUser
        })
        interviewing = db.Apps.count_documents({
            "status": "Interviewing",
            "user": loggedUser
        })
        rejected = db.Apps.count_documents({
            "status": "Rejected",
            "user": loggedUser
        })

        return render_template("home.html",
                               week=len(docs_week),
                               month=len(docs_month),
                               total=total,
                               accepted=accepted,
                               interviewing=interviewing,
                               rejected=rejected)

    # edit profile page
    @app.route('/edit-profile', methods=['GET', 'POST'])
    def edit_profile():
        user = db.Users.find_one({"_id": loggedUser})

        # post request
        if request.method == 'POST':
            new_name = request.form.get('newUsername')

            # update the database
            db.Users.update_one({"_id": ObjectId(loggedUser)},
                                {"$set": {
                                    "username": new_name
                                }})

            return redirect(url_for('edit_profile'))

        # get request
        return render_template("edit-profile.html", user=user)

    # job tracking page
    @app.route('/track', methods=['GET', 'POST'])
    def track():
        # post request
        if request.method == 'POST':
            # get user input from search bar
            choice = request.form.get('status')

            if choice.lower() in 'applied interviewing rejected':
                applications = db.Apps.find({
                    "user": loggedUser,
                    "status": choice
                })
            elif choice.lower() == 'descending':
                applications = db.Apps.find({
                    "user": loggedUser
                }).sort("date", -1)
            elif choice.lower() == 'ascending':
                applications = db.Apps.find({
                    "user": loggedUser
                }).sort("date", 1)

            return render_template("track.html", applications=applications)

        # get request
        applications = db.Apps.find({"user": loggedUser})
        return render_template("track.html", applications=applications)

    # delete app
    @app.route('/delete', methods=['GET', 'POST'])
    def delete():
        # post request
        # if request.method == 'POST':
        db.Apps.delete_one({"_id": ObjectId('67bdf16a3028f7eee227824d')})

        applications = db.Apps.find({"user": loggedUser})
        return render_template("delete.html", applications=applications)

    @app.errorhandler(Exception)
    def handle_error(e):
        """
        Output any errors - good for debugging.
        Args:
            e (Exception): The exception object.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("error.html", error=e)

    return app


app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
