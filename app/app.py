#later get rid of unused modules
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, session
from dotenv import load_dotenv 
import os
import pymongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bson.objectid import ObjectId

#loading env file
load_dotenv()

#verify environmental variables
if not os.getenv("MONGO_URI") or not os.getenv("SECRET_KEY") or not os.getenv("MONGO_DBNAME"):
    raise ValueError("Missing required environment variable.")

#app setup
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

#initialize login manager and necessary objects
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

#mongodb setup
mongo = pymongo.MongoClient(os.getenv("MONGO_URI"), ssl = True)
db = mongo[os.getenv("MONGO_DBNAME")]
users = db.users
recipes = db.recipes

#verify mongodb connection
try:
    mongo.admin.command("ping")
    print("Connected to MongoDB")
except Exception as exception:
    print("MongoDB connection error:", exception)

#user class for login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]

#user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #check if user already exists
        if users.find_one({"username": username}):
            return "User already exists"

        #hash password and store user
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user_id = users.insert_one({"username": username, "password": hashed_password}).inserted_id
        return redirect(url_for("login"))

    return render_template("register.html")

#user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = users.find_one({"username": username})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/your_recipes')
@login_required
def your_recipes():
    return render_template('your_recipes.html', recipes=recipes)


@app.route('/add_delete', methods=['GET', 'POST'])
@login_required
def add_delete():
    if request.method == "POST":
        if request.form['action'] == 'add':
            recipe_name = request.form['recipe_name']
            ingredient_list = request.form['ingredient_list'].split(',')
            cooking_supplies = request.form['cooking_supplies'].split(',')
            instructions = request.form['instructions']

            db.recipes.insert_one({
                'user_id': current_user.id,
                'recipe_name': recipe_name,
                'ingredient_list': ingredient_list,
                'cooking_supplies': cooking_supplies,
                'instructions': instructions
                
            })

            return redirect(url_for('add_delete'))
            
        elif request.form['action'] == 'delete':
            recipe_id = request.form['recipe_id']

            db.recipes.delete_one({
                '_id': ObjectId(recipe_id),
                'user_id': current_user.id
                
            })

            return redirect(url_for('add_delete'))

    recipes = db.recipes.find({"user_id": current_user.id})
    return render_template('add_delete.html', recipes=recipes)

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)
