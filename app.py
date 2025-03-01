import os
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv, dotenv_values
from datetime import datetime

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
        return render_template("home.html")
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            doc = db.users.find_one({"email": email})
            if doc:
                redirect(url_for("register"))
            else: 
                db.users.insert_one({
                    "email": email,
                    "password": password
                })

                return redirect(url_for("login"))

        return render_template("register.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("login.html")
    
    @app.route("/logout")
    def logout():
        return redirect(url_for("login"))
    
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

        events = list(db.events.find({
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"date": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}},
                {"location": {"$regex": search_term, "$options": "i"}},
                {"category": {"$regex": search_term, "$options": "i"}}
            ]
        }))

        sorted_events = sorted(events, key=lambda obj: datetime.strptime(obj["date"], "%m/%d/%Y"))
        print(sorted_events)

        return render_template("search.html", searchterm=search_term, events=sorted_events)
    
    @app.errorhandler(Exception)
    def handle_error(e):
        """
        Route for GET requests to any errors
        Returns: render_template (html for error page)
        """
        return render_template("error.html", error=e)
    
    return app


app = create_app()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)