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

#load_dotenv()
#uri = os.getenv("MONGO_URI")
#Mongo_DBNAME= os.getenv("MONGO_DBNAME")
#lient = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
#acess database
#create DB/Acess
#myDb= client["DuoProject"]
#List of data Tables
#myTable= myDb["users"]
#AssigmentsTable= myDb["Assigments"]

######## USER AUTHENTICATION
##password autheenction
#user

##
## Function: returning user password authentication
## Usage: query the user table. given a username and password, determine if the user exists and the password matches. 
##          If login is valid, return the user ID
##          If login is not valid, return None
## 
def pwd_auth(myDb,username, password):
    print("Hello World")
    usertable= myDb["users"] 
    exist= usertable.find_one({"username":username,"password":password})
    if exist:
        return exist["_id"]
    else:
        return None
    #return None





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
    #get name from user database and user id
   # Data_Base= myDb["users"] 
   # exist= Data_Base.find_one({"_id":userID})
   # use_id= exist["_id"]
    AsTable= mydb["Assigments"]
    deadlines = AsTable.find({"user_ID":ObjectId(userID)})
    return deadlines
    #acess Assigments

    #return None



##
## Function: get classes
## Usage: get all classes belonging to a specific user
## 
def get_classes(mydb, userID):
    ClassTable= mydb["Class"]
    Classes= ClassTable.find({"USER_id":userID})
    return  Classes 


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
    usertable = mydb["Assigments"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(assignmentID)
    })

    print("testing", exist)

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(assignmentID)
        })
        
        return result.deleted_count
    
    else:
        print("Assignment not found.")
        return 0

##
## Function: delete an exam
## Usage: delete an exam from the database
## 
def delete_exam(mydb, userID, examID):
    usertable= mydb["Exams"]

    exist = usertable.find_one({
        "username":userID,
        "exam":examID
    })

    if exist:
        return usertable.delete_one({
            "username":userID,
            "exam":examID
        })
    
    else:
        return print (0)


##
## Function: delete a study session
## Usage: delete a study session from the database
## 
def delete_study_session(mydb, userID, study_sessionID):
    usertable= mydb["Studies"]

    exist = usertable.find_one({
        "username":userID,
        "study_session":study_sessionID
    })

    if exist:
        return usertable.delete_one({
            "username":userID,
            "study_session":study_sessionID
        })
    
    else:
        return print (0)


##
## Function: delete a task
## Usage: delete a task from the database
## 
def delete_task(mydb, userID, taskID):
    usertable= mydb["Tasks"]

    exist = usertable.find_one({
        "username":userID,
        "task":taskID
    })

    if exist:
        return usertable.delete_one({
            "username":userID,
            "task":taskID
        })
    
    else:
        return print (0)

##
## Function: delete a class
## Usage: delete a class from the database
## 
def delete_class(mydb, userID, classID):
    usertable= mydb["Class"]
    exist = usertable.find_one({
        "username":userID,
        "class":classID
    })

    if exist:
        return usertable.delete_one({
            "username":userID,
            "class":classID
        })
    else:
        return print (0)



######## EDIT FUNCTIONS


##
## Function: edit user info
## Usage: edit user info in user table according to specifications
## 
def edit_profile(mydb, userID, password, bio, pic, dark_mode):
    return None
