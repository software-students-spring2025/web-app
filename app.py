from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv, dotenv_values
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import certifi
import flask_login
import flask
import hashlib

load_dotenv()

app = Flask(__name__)
app.config['SESSION_PROTECTION'] = "strong"
app.secret_key = "user_creds_k3ys"

#login 
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#app configs
config = dotenv_values()
app.config.from_mapping(config)

#mongodb client
client = pymongo.MongoClient(os.getenv("MONGO_URI"), ssl_ca_certs=certifi.where())
db = client[os.getenv("MONGO_DBNAME")]
tv_shows_collection = db.tv_shows
users = db.user_creds

class User(flask_login.UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.password = user_doc["password"]
        #self.password = hashlib.sha256(user_doc["password"]).hexdigest()


    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(username):
    record = users.find_one({"username": username})
    if not record:
        return
    
    return User(record)


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')

    if not username:
        return
    
    user_doc = users.find_one({"username": username})

    if not user_doc: #user doesn't exist
        return None

    return User(user_doc)

@app.route("/home")
def home():
    if "user" in session:
        return render_template("home.html", username=session["user"])
    episodes = db.tv_shows.find({}).sort("date", -1)
    return render_template("home.html", episodes=episodes)

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        entered_pw = request.form.get('password')

        if not username or not entered_pw:
            flash("Username and password are required", "danger")
            return redirect(url_for("login"))
    
        user_doc = users.find_one({"username": username})
        #password = users.find({"username": username})

        if user_doc and (entered_pw == user_doc["password"]): #correct credentials
            user = User(user_doc)
            #user.username = username
            flask_login.login_user(user)
            session["user"] = user.id
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html")
        
    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = users.find_one({"username": username})
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("signup")) #, "Username already exists", "danger"

        #hashed_pw = hashlib.sha256(password).hexdigest()
        new_doc = db.users.insert_one({"username": username, "password": password})
        user_id = str(new_doc.inserted_id)
        return redirect(url_for("login")) #, message="Sign up successful! You can now log in."
    return render_template("signup.html")

#add entry page
@app.route("/add", methods=["GET", "POST"])
def add():
    #get data from HTML form
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        season = request.form.get("season")
        episode = request.form.get("episode") 
        rating = request.form.get("rating") 
        date = request.form.get("date")
        tags = request.form.get("tags").split(",")
        comment = request.form.get("comment") 

        #episode = f"S{season}E{episode_num}" if season and episode_num else ""

        new_episode = {
            "title": title,
            "genre": genre,
            "season": season,
            "episode": episode,
            "rating": int(rating or 0),
            "tags": [tag.strip() for tag in tags],
            "date": date,
            "comment": comment,
        }

        #insert data into user collection (may need to change, possibly inefficient for large num of users)
        db.tv_shows.insert_one(new_episode)
        return redirect(url_for("success"))

    return render_template("add_show.html")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if query:
        results = tv_shows_collection.find({"title": {"$regex": query, "$options": "i"}})
        shows = [
            {
                "id": str(show["_id"]),
                "title": show["title"],
                "genre": show.get("genre", ""),
                "season": show.get("season" ""),
                "episode": show["episode"],
                "rating": show["rating"],
                "tags": show.get("tags", []),
                "comment": show.get("comment", ""),
            }
            for show in results
        ]
        return render_template("home.html", episodes=shows)

    return render_template("home.html", episodes=[])

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        # Get the show_id from the form
        show_id = request.form["show_id"]
        
        if show_id:
            try:
                tv_shows_collection.delete_one({"_id": ObjectId(show_id)})
                return render_template("success.html", message="Episode deleted successfully!")
            except Exception as e:
                return render_template("success.html", message=f"Error deleting show: {e}")

    # If it's a GET request, display the list of shows
    shows = tv_shows_collection.find()
    return render_template("delete.html", shows=shows)

"""
@app.route("/login")
def login():
    db.credentials. =
    if 
"""

@app.route("/success")
def success():
    return "Episode added successfully!"

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
