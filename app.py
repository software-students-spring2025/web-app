import os
from flask import Flask, render_template, request
import pymongo
from dotenv import load_dotenv, dotenv_values

# load environment variables from .env file
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

    # create a new client and connect to the server
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DBNAME")]

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print(" * Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    @app.route("/")
    def show_home():
        return "<h1>Dashboard</h1>"
    
    @app.route("/add")
    def show_add():
        return render_template("addEvent.html")
    
    @app.route("/details")
    def show_details():
        return render_template("details.html")
    
    @app.route("/edit")
    def show_edit():
        return render_template("edit.html")
    
    @app.route("/search")
    def show_search():
        """
        Route for GET requests to the search page
        Accepts a search term and displays the results 
        Returns: render_template (html for search page)
        """
        search_term = request.args.get("searchterm", "")
        print(search_term)
        events = db.events.find({
            "$or": [
                {"name": {"$options": "i", "$regex": search_term}},
                {"date": {"$regex": search_term}},
                {"location": {"$options": "i", "$regex": search_term}},
                {"category": {"$options": "i", "$regex": search_term}}
            ]
        })
        return render_template("search.html", searchterm=search_term, events=events)
    
    @app.errorhandler(Exception)
    def handle_error(e):
        return render_template("error.html", error=e)
    
    return app


app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)