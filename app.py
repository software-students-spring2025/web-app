import os
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import flask_login

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

    # flask-login setup
    login_manager = flask_login.LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    # user class
    class User(flask_login.UserMixin):
        def __init__(self, user):
            self.id = str(user["_id"])  
            self.email = user["email"]


    @login_manager.user_loader
    def user_loader(email):
        user = db.users.find_one({"_id": ObjectId(email)})
        if user:
            return User(user)
        return None
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get("email")
        if email:
            user = db.users.find_one({"email": email})
            if user:
                return User(user)
        return None

    @app.route("/home")
    def show_home():
        user_id = flask_login.current_user.id

        events = list(db.events.find({"user_id": user_id}))

        events.sort(key=lambda event: datetime.strptime(event["date"], "%m/%d/%Y"))

        return render_template('home.html', events=events)
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            doc = db.users.find_one({"email": email})
            if doc:
                error = "Email is already in use"
                return render_template("register.html", error=error)
            else: 
                db.users.insert_one({
                    "email": email,
                    "password": password
                })

                return redirect(url_for("login"))

        return render_template("register.html")
    
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = db.users.find_one({"email": email})
            if user and user.get("password") == password:
                user_obj = User(user)
                flask_login.login_user(user_obj)
                return redirect(url_for("show_home"))
            else:
                error = "Incorrect email or password"
                return render_template("login.html", error = error)
        else:
            return render_template("login.html")
    
    @app.route("/logout")
    def logout():
        flask_login.logout_user()
        return redirect(url_for("login"))
    
    @app.route("/add", methods=["GET", "POST"])
    def add_event():
        if request.method == "POST":
            user_id = flask_login.current_user.id
        
            event = {
                "user_id": user_id,
                "name": request.form["name"],
                "date": request.form["date"],
                "time": request.form["time"],
                "location": request.form["location"],
                "category": request.form["category"],
                "description": request.form["description"],
            }
            db.events.insert_one(event)  
            return redirect(url_for("show_home"))  
        return render_template("addEvent.html")
    
    @app.route("/edit/<event_id>", methods=["GET", "POST"])
    def edit_event(event_id):
        user_id = flask_login.current_user.id

        event = db.events.find_one({"_id": ObjectId(event_id), "user_id": user_id})

        if not event:
            return "Event not found", 404  # Handle missing event
        
        if request.method == "POST":
            updated_event = {
                "name": request.form["name"],
                "date": request.form["date"],
                "time": request.form["time"],
                "location": request.form["location"],
                "category": request.form["category"],
                "description": request.form["description"],
            }
            db.events.update_one({"_id": ObjectId(event_id)}, {"$set": updated_event})
            return redirect(url_for("show_home"))

        return render_template("edit.html", event=event)
    
    @app.route("/details/<event_id>")
    def show_details(event_id):
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if event is None:
            return "Event not found", 404  # Handle missing event

        return render_template("details.html", event=event)
    
    @app.route("/delete/<event_id>")
    def delete_event(event_id):
        user_id = flask_login.current_user.id

        result = db.events.delete_one({"_id": ObjectId(event_id), "user_id": user_id})
        
        if result.deleted_count == 0:
            return "Unauthorized: You can only delete your own events", 403  # Forbidden error
    
        return redirect(url_for("show_home"))
    
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