from flask import Flask, render_template, request, url_for, redirect, session
#import pymongo
from bson.objectid import ObjectId
import database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi
from dotenv import load_dotenv
from flask_session import Session

'''
notes / instructions

run app.py, then go to 127.0.0.1:5000 in browser

'''

# load environment variables 
load_dotenv()

# connect MongoDB
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
Mongo_DBNAME= os.getenv("MONGO_DBNAME")
myDb= client[Mongo_DBNAME]

# start app
app = Flask(__name__)

# start new user session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "mongodb"
Session(app)



# homepage / dashboard
@app.route("/", methods=('GET', 'POST'))
def show_dashboard():
    # show the dashboard
    if request.method == "GET":   
        print('cookies', request.cookies)
        # if we are logged in (uid cookie has been set) - load the dashboard page
        if 'uid' in request.cookies:
            data = {
                "deadlines": [
                    {"name": 'example deadline 1', "date": "March 1"}, 
                    {"name": 'example deadline 2', "date": "March 2"}
                ], 
                "classes": [], 
                "tasks": []
            }
            return render_template('dashboard.html', data=data) # render home page template 
        # if we are NOT logged in - redirect to login
        return redirect(url_for('show_login'))
    # form handling
    elif request.method == "POST":
        pass  

    
    return render_template('dashboard.html') # render home page template 

# login
@app.route("/login", methods=('GET', 'POST'))
def show_login():
    # simply show the blank login page
    if request.method == "GET":   
        return render_template('signin.html') # render home page template 
    
    # if information has been submitted to login: 
    elif request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        ## 
        ## authenticate the username and password
        ##

        # set the uid cookie as the value of the user id
        # redirect to the dashboard
        response = redirect(url_for('show_dashboard'))
        response.set_cookie('uid', uname)
        return response
    
# sign up / new account
@app.route("/signup", methods=("GET", "POST"))
def show_signup():
    # simply show the blank signup page
    if request.method == "GET":   
        return render_template('signup.html') # render home page template 
    
    # if information has been submitted to signup: 
    elif request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        ## 
        ## authenticate the username and password, create new user in mongo
        ##

        # set the uid cookie as the value of the user id
        # redirect to the dashboard
        response = redirect(url_for('show_dashboard'))
        response.set_cookie('uid', uname)
        return response

# profile
@app.route("/profile", methods=("GET", "POST"))
def show_profile():
    # simply show the profile page
    if request.method == "GET":   
        #user_data = database.get_user_info(myDb)
        data = {
            "user": {
                "userID": "",
                "name": "John Doe",
                "age": 25,
                "username": "John", 
                "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vitae urna euismod, blandit felis at, suscipit orci."
            }
        }
        
        return render_template('profile.html', data=data) # render home page template 
    
    # 
    elif request.method == "POST":
        pass

# sign out
@app.route("/logout", methods=["GET"])
def logout():
    # DELETE the uid cookie 
    # redirect to the login page
    response = redirect(url_for('show_login'))
    response.delete_cookie("uid")
    return response

# edit profile
@app.route("/profile-edit", methods=["POST"])
def edit_profile():
    pic = request.form['pic']
    name = request.form['name']
    age = request.form['age']
    bio = request.form['bio']
    print("profile edited in backend")
    data = {
        "user": {
            "userID": "",
            "name": name,
            "age": age,
            "username": "John", 
            "bio": bio
        }
    }
    return redirect(url_for('show_profile'))


# keep alive
if __name__ == "__main__":
    app.run(debug=True) #running your server on development mode, setting debug to True
