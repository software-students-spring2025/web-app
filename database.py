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


######## USER AUTHENTICATION


##
## Function: returning user password authentication
## Usage: query the user table. given a username and password, determine if the user exists and the password matches. 
##          If login is valid, return the user ID
##          If login is not valid, return None
## 
def pwd_auth(mydb, username, password):
    return None


##
## Function: new user creation
## Usage: query the user table, check for validity
##          If username already exists, return None
##          If username is new, create a new user entry in the data table and return the user ID
## 
def new_account(mydb, username, password):
    return None



######## GET FUNCTIONS



##
## Function: get deadlines
## Usage: get all deadlines belonging to a specific user
## 
def get_deadlines(mydb, userID):
    return None


##
## Function: get classes
## Usage: get all classes belonging to a specific user
## 
def get_classes(mydb, userID):
    return None


##
## Function: get study sessions
## Usage: get all study sessions belonging to a specific user
## 
def get_study_sessions(mydb, userID):
    return None


##
## Function: get tasks
## Usage: get all current tasks belonging to a specific user
## 
def get_tasks(mydb, userID):
    return None


##
## Function: get info associated with a user
## Usage: get all account info belonging to a specific user
## 
def get_user_info(mydb, userID):
    return None



######## DELETE FUNCTIONS


##
## Function: delete an assignment
## Usage: delete an assignment from the database
## 
def delete_assignment(mydb, userID, assignmentID):
    return None


##
## Function: delete an exam
## Usage: delete an exam from the database
## 
def delete_exam(mydb, userID, examID):
    return None


##
## Function: delete a study session
## Usage: delete a study session from the database
## 
def delete_study_session(mydb, userID, study_sessionID):
    return None


##
## Function: delete a task
## Usage: delete a task from the database
## 
def delete_task(mydb, userID, taskID):
    return None


##
## Function: delete a class
## Usage: delete a class from the database
## 
def delete_class(mydb, userID, classID):
    return None



######## EDIT FUNCTIONS


##
## Function: edit user info
## Usage: edit user info in user table according to specifications
## 
def edit_profile(mydb, userID, password, bio, pic, dark_mode):
    return None
