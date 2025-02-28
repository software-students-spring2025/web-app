from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
import flask_login
import os
import pymongo

#load env variables
load_dotenv()
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_URI = os.getenv('MONGO_URI')

# make a connection to the database server
connection = pymongo.MongoClient(MONGO_URI)
# select a specific database on the server
db = connection["Jitter"]

'''
tempdoc = {
    "name": "Foo Barstein",
    "email": "fb1258@nyu.edu",
}
'''
mongoid = db.employer.insert_one(tempdoc)

'''
#set up flask app
app = Flask(__name__)
app.secret_key = 'secret-key'

#instantiate login manager and pass it the app
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user



#temp home route
@app.route('/')
def hello_world():
    print("hello world")

'''