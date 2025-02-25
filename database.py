'''
This file contains custom helper functions necessary to load, process, and handle data from the MongoDB database

These functions are intended to be called by the main Flask application (app.py) and returned to it for use
'''
#import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import certifi
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
#import datetime
load_dotenv()
uri = os.getenv("MONGO_URI")
Mongo_DBNAME= os.getenv("MONGO_DBNAME")
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
#acess database
#create DB/Acess
myDb= client["DuoProject"]
#create table
myTable= myDb["users"]

######## USER AUTHENTICATION


##
## Function: returning user password authentication
## Usage: query the user table. given a username and password, determine if the user exists and the password matches. 
##          If login is valid, return the user ID
##          If login is not valid, return None
## 
def pwd_auth(username, password):
    return None


##
## Function: new user creation
## Usage: query the user table, check for validity
##          If username already exists, return None
##          If username is new, create a new user entry in the data table and return the user ID
## 
def new_account(username, password):
    return None



######## GET FUNCTIONS



##
## Function: get deadlines
## Usage: get all deadlines belonging to a specific user
## 
def get_deadlines(username):
    return None


##
## Function: get classes
## Usage: get all classes belonging to a specific user
## 
def get_classes(username):
    return None


##
## Function: get study sessions
## Usage: get all study sessions belonging to a specific user
## 
def get_study_sessions(username):
    return None


##
## Function: get tasks
## Usage: get all current tasks belonging to a specific user
## 
def get_tasks(username):
    return None


##
## Function: get info associated with a user
## Usage: get all account info belonging to a specific user
## 
def get_user_info(username):
    return None



######## DELETE FUNCTIONS


##
## Function: delete a deadline
## Usage: delete a deadline from the database
## 
def delete_deadline(username, deadline):
    return None


##
## Function: delete a study session
## Usage: delete a study session from the database
## 
def delete_study_session(username, study_session):
    return None


##
## Function: delete a task
## Usage: delete a task from the database
## 
def delete_task(username, study_session):
    return None


##
## Function: delete a class
## Usage: delete a class from the database
## 
def delete_class(username, study_session):
    return None



######## EDIT FUNCTIONS


##
## Function: edit user info
## Usage: edit user info in user table according to specifications
## 
def edit_profile(username, password, bio, pic, age):
    return None
