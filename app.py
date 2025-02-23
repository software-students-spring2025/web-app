from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


client = MongoClient("mongodb+srv://xl4358:linxiangyu2004@project2-blabla.zeyv4.mongodb.net/?retryWrites=true&w=majority&appName=project2-blabla")
db = client["users"]     
users_collection = db["users"] 

# default landing page: login 
@app.route("/")
def index():
    return render_template("index.html")

# register page
@app.route("/signup")
def register():
    return render_template("signup.html")

# add dream page
@app.route("/add_dream", methods=["GET", "POST"])
def add_dream():
    return render_template("add_dream.html")

# home page
@app.route("/home")
def home():
    return render_template("home.html")

# analysis page
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

#edit_dream page
@app.route("/edit_dream")
def edit_dream():
    tags = ["Happy", "Funny", "Excited", "XXXX"]
    return render_template("edit_dream.html", tags=tags)

if __name__ == "__main__":
    app.run(debug=True)
