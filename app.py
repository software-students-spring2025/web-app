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
app = Flask(__name__, static_folder='assets')

# start new user session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "mongodb"
Session(app)



# homepage / dashboard
@app.route("/", methods=('GET', 'POST'))
def show_dashboard():

    # if we are NOT logged in - redirect to login
    if 'userid' not in session or session['userid'] is None:
        return redirect(url_for('show_login'))

    # if we are logged in (session["userid"] is not None) - load the dashboard page
    # show the dashboard
    if request.method == "GET":   

        if 'userid' in session and session['userid'] is not None:
            data = {
                "user": database.get_user_info(myDb, ObjectId(session['userid'])),
                "deadlines": database.get_deadlines(myDb, ObjectId(session['userid'])), 
                "classes": database.get_classes(myDb, ObjectId(session['userid'])), 
                "tasks": database.get_tasks(myDb, ObjectId(session['userid'])) 
            }
            print(data["deadlines"])
            return render_template('dashboard.html', data=data) # render home page template 
        
        
        
    
    # form handling
    elif request.method == "POST":
        pass  

    return render_template('dashboard.html') # render home page template 


# study session page
@app.route("/study", methods=('GET', 'POST'))
def show_study():

    # if we are NOT logged in - redirect to login
    if 'userid' not in session or session['userid'] is None:
        return redirect(url_for('show_login'))

    # show study session page
    if request.method == 'GET':
        data = {
                "user": database.get_user_info(myDb, ObjectId(session['userid'])),
                "deadlines": database.get_deadlines(myDb, ObjectId(session['userid'])), 
                "classes": database.get_classes(myDb, ObjectId(session['userid'])), 
                "tasks": database.get_tasks(myDb, ObjectId(session['userid'])), 
                "study-sessions": database.get_study_sessions(myDb, ObjectId(session['userid']))
            }
        return render_template('study_session.html', data=data) # render home page template 


# login
@app.route("/login", methods=('GET', 'POST'))
def show_login():
    # simply show the blank login page
    if request.method == "GET":   
        return render_template('signin.html', data={"error": ""}) # render home page template 
    
    # if information has been submitted to login: 
    elif request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        
        # authenticate the username and password
        uid = database.pwd_auth(myDb, uname, pwd)

        # incorrect username/password: reload page
        if uid is None:
            return render_template('signin.html', data={"error": "The username or password entered is incorrect."})

        # correct username/password: redirect to the dashboard
        session["userid"] = str(uid)
        return redirect(url_for('show_dashboard'))
    

# sign up / new account
@app.route("/signup", methods=("GET", "POST"))
def show_signup():
    # simply show the blank signup page
    if request.method == "GET":   
        return render_template('signup.html', data={"error": ""}) # render home page template 
    
    # if information has been submitted to signup: 
    elif request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        
        # try new account creation
        uid = database.new_account(myDb, uname, pwd)

        # if unsuccessful (user already exists)
        if uid is None: 
            return render_template('signup.html', data={"error": "This username is taken"})

        # set session variables
        # redirect to the dashboard
        session["userid"] = str(uid)
        return redirect(url_for('show_dashboard'))
    

# profile
@app.route("/profile", methods=("GET", "POST"))
def show_profile():

    # if we are NOT logged in - redirect to login
    if 'userid' not in session or session['userid'] is None:
        return redirect(url_for('show_login'))
    
    # simply show the profile page
    if request.method == "GET":   
        
        data = {
            "user": database.get_user_info(myDb, ObjectId(session['userid']))
        }
        return render_template('profile.html', data=data) # render profile page template 
    
    # 
    elif request.method == "POST":
        pass


# sign out
@app.route("/logout", methods=["GET"])
def logout():
    # edit session variables
    # redirect to the login page
    session["userid"] = None
    return redirect(url_for('show_login'))


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
