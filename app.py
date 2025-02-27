import os
from flask import Flask, render_template, request, redirect, url_for
import pymongo 
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()

def create_app(): 
    app = Flask(__name__)

    config = dotenv_values()
    app.config.from_mapping(config)

    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e: 
        print(" * MongoDB connection error:", e)
    
    @app.route("/")
    def home(): 
        return render_template('homescreen') # Add the correct name for template

    @app.route("/logout")
    def logout():
        # There may be some code in regards to Flask Login 
        return render_template('logoutScreen') # Add the correct name for template

    @app.route("/goHome")
    def goHome():
        return redirect(url_for('home'))

    @app.route("/showBoth")
    def showBoth():
        docs = 0 # Add correct Database call (get all docs in the database to display)
        return render_template('showBothScreen' , docs = docs) # Add the correct name for template

    @app.route("/create/<dbType>" , methods=["POST"])
    def create_post(dbType):

        # Get the values from the fields 
        # Make a document and import it into the Database

        return redirect(url_for('showBoth'))

    @app.route("/edit/<post_id>")
    def edit(post_id): 

        docs = 0 # Add correct Database call (Find the document from Database from the post_id)

        return render_template('editDocument', docs=docs) # Add the correct name for template

    @app.route("/edit/<post_id>/<dbType>" , methods = ["POST"])
    def edit_post(post_id, dbType):
        
        # Get the values from the fields 
        # Make a document and import it into the Database

        return redirect(url_for('showBoth'))

    @app.route("/delete/<post_id>")
    def delete(post_id):

        # Delete the document from the Database

        return redirect(url_for('showBoth'))

    @app.errorhandler(Exception)
    def handle_error(e): 

        return render_template("error.html", error=e) # Add the correct name for template

    app = create_app()