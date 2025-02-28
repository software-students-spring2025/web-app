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

def pwd_auth(mydb,username, password):
    print("Hello World")
    usertable= mydb["users"] 
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
#works 
def new_account(mydb, username, password):
    #print("Hello new account")
    acconttable= mydb["users"]
    exist = acconttable.find_one({"username": username})

    if exist:
       # print("User found:")
        return None
    else:
        newuser= {
            "username": username, "password": password
        }
        acconttable.insert_one(newuser)
        r=  acconttable.find_one({"username": username, "password": password},{"_id":1})
       # print(r["_id"])
       # print(result.inserted_id)
    return r["_id"]
    



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
    asTable= mydb["Assigments"]
    deadlines = asTable.find({"user_ID":ObjectId(userID)})
    deadlines_dict= [doc for doc in deadlines]
    return deadlines_dict
    #acess Assigments

    #return None



##
## Function: get classes
## Usage: get all classes belonging to a specific user
## works
def get_classes(mydb, userID):
    classTable= mydb["Class"]
    classes= classTable.find({"user_ID":ObjectId(userID)})
    classes_dict= [doc for doc in classes]
    return  classes_dict


##
## Function: get study sessions
## Usage: get all study sessions belonging to a specific user
## works
def get_study_sessions(mydb, userID):
    studyTable= mydb["Studies"]
    study= studyTable.find({"user_id":ObjectId(userID)})
    study_dict= [doc for doc in study]
    return study_dict


##
## Function: get tasks
## Usage: get all current tasks belonging to a specific user
##  return that tasks but will have to loop through in order to print each tasks
#works
def get_tasks(mydb, userID):
    tasktable = mydb["Tasks"]
    tasks=tasktable.find({"user_id":ObjectId(userID)})
    task_dict= [doc for doc in tasks]
    return task_dict


##
## Function: get info associated with a user
## Usage: get all account info belonging to a specific user
## return poy cursor can turn into a list if need be
def get_user_info(mydb, userID):
   usetable= mydb["users"]
   user=  usetable.find({"_id":ObjectId(userID)})
   user_dict= [doc for doc in user]
   return  user_dict

 

##### ADD FUNCTIONS


# Usage: add a class to the users profile. Front end needs to collect all the parameters that the function requires and call in the format MongoDB shows
# Return: 0 if there was an error adding the new class or 1 if the process was completed without issues
def add_class(mydb, userID, name):
    usertable = mydb["Class"]
    
    exist = usertable.find_one({
        "user_ID" : ObjectId(userID),
        "name" : name
    })

    if (exist):
        print("Class already exists")
        return (0)
    
    else:
        doc = {
            "user_ID" : ObjectId(userID),
            "name" : name,
            "time_studied_hours" : 0
        }

        usertable.insert_one(doc) # Creation of the class will assign it a unique ID and if needed can be equated to a variable

        return (1)
    
# Usage: adds a deadline for a specific class of a specific type to the users profile. Front end needs to collect all the parameters that the function requires and call in the format MongoDB shows
# Return: 0 if there was an error adding the new deadline or 1 if the process was completed without issues
def add_deadlines(mydb, userID, classID, due_date, name, type):
    usertable = mydb["Deadline"]
    
    exist = usertable.find_one({
        "user_ID" : ObjectId(userID),
        "class_ID" : ObjectId(classID),
        "due_date" : due_date, # Note Due Dates have to be in this format: 2025-03-05T05:00:00.000+00:00
        "name" : name,
        "type" : type
    })

    if (exist):
        print("Deadline already exists")
        return (0)
    
    else:
        doc = {
            "user_ID" : ObjectId(userID),
            "class_ID" : ObjectId(classID),
            "due_date" : due_date, 
            "name" : name,
            "type" : type
        }

        usertable.insert_one(doc) # Creation of the deadline will assign it a unique ID and if needed can be equated to a variable

        print("Deadline created!")
        return (1)
    
# Usage: adds a exam date for a specific class to the users profile. Front end needs to collect all the parameters that the function requires and call in the format MongoDB shows
# Return: 0 if there was an error adding the new exam or 1 if the process was completed without issues
def add_exams(mydb, userID, classID, date, topics):
    usertable = mydb["Exams"]
    
    exist = usertable.find_one({
        "user_ID" : ObjectId(userID),
        "class_ID" : ObjectId(classID),
        "date" : date, # Note date has to be in this format: 2025-03-05T05:00:00.000+00:00
        "topics" : topics
    })

    if (exist):
        print("Exam already exists")
        return (0)
    
    else:
        doc = {
            "user_ID" : ObjectId(userID),
            "class_ID" : ObjectId(classID),
            "date" : date, # Note date has to be in this format: 2025-03-05T05:00:00.000+00:00
            "topics" : topics,
        }

        usertable.insert_one(doc) # Creation of the deadline will assign it a unique ID and if needed can be equated to a variable

        print("Exam created!")
        return (1)

# Usage: adds a study session for a specific class to the users profile. Front end needs to collect all the parameters that the function requires and call in the format MongoDB shows
# Return: 0 if there was an error adding the new study session or 1 if the process was completed without issues
def add_study_session(mydb, userID, classID, date, duration, goals):
    usertable = mydb["Studies"]
    
    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "class_ID": ObjectId(classID),
        "date": date,
        "duration_hours" : duration,
        "goals_completed": {"$all": goals}  # Ensures all goals exist in the array
    })

    if (exist):
        print("Study session already exists")
        return (0)
    
    else:
        doc = {
            "user_ID" : ObjectId(userID),
            "class_ID" : ObjectId(classID),
            "date" : date, # Note date has to be in this format: 2025-03-05T05:00:00.000+00:00
            "duration_hours" : duration,
            "goals_completed" : goals
        }

        usertable.insert_one(doc) # Creation of the study_session will assign it a unique ID and if needed can be equated to a variable

        print("Study session created!")
        return (1)

# Usage: adds a task for a specific class to the users profile. Front end needs to collect all the parameters that the function requires and call in the format MongoDB shows
# Return: 0 if there was an error adding the new task or 1 if the process was completed without issues
def add_tasks(mydb, userID, name):
    usertable = mydb["Tasks"]
    
    exist = usertable.find_one({
        "user_ID" : ObjectId(userID),
        "name" : name
    })

    if (exist):
        print("Task already exists!")
        return (0)
    
    else:
        doc = {
            "user_ID" : ObjectId(userID),
            "name" : name,
        }

        usertable.insert_one(doc) # Creation of the Task will assign it a unique ID and if needed can be equated to a variable

        print("Task created!")
        return (1)






######## DELETE FUNCTIONS


##
## Function: delete an assignment
## Usage: delete an assignment from the database
## 
def delete_deadline(mydb, userID, deadlineID):
    usertable = mydb["Deadline"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(deadlineID)
    })

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(deadlineID)
        })
        
        return result
    
    else:
        print("Assignment not found.")
        return 0

##
## Function: delete an exam
## Usage: delete an exam from the database
## 
def delete_exam(mydb, userID, examID):
    usertable = mydb["Exams"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(examID)
    })

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(examID)
        })
        
        return result
    
    else:
        print("Exam not found.")
        return 0


##
## Function: delete a study session
## Usage: delete a study session from the database
## 
def delete_study_session(mydb, userID, study_sessionID):
    usertable = mydb["Studies"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(study_sessionID)
    })

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(study_sessionID)
        })
        
        return result
    
    else:
        print("Study session not found.")
        return 0


##
## Function: delete a task
## Usage: delete a task from the database
## 
def delete_task(mydb, userID, taskID):
    usertable = mydb["Tasks"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(taskID)
    })

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(taskID)
        })
        
        return result
    
    else:
        print("Tasks not found.")
        return 0

##
## Function: delete a class
## Usage: delete a class from the database
## 
def delete_class(mydb, userID, classID):
    usertable = mydb["Class"]

    exist = usertable.find_one({
        "user_ID": ObjectId(userID),
        "_id": ObjectId(classID)
    })

    if exist:
        result = usertable.delete_one({
            "user_ID": ObjectId(userID),
            "_id": ObjectId(classID)
        })
        
        return result
    
    else:
        print("Class not found.")
        return 0



######## EDIT FUNCTIONS


##
## Function: edit user info
## Usage: edit user info in user table according to specifications
## 
def edit_profile(mydb, userID, password, bio, pic, dark_mode):
    return None


#Update User
def edit_study(mydb,userID,studyID,date=None,goals=None,duration_hours=None):
    usetable= mydb["Studies"]
    user=  usetable.find_one({"user_id":ObjectId(userID),"_id":ObjectId(studyID)})
    if not user:
        print("no user")
        return None 
    updates= {}
    if date is not None:
        print("date update")
        updates["date"]= date 
    if goals is not None:
        print("print goal update")
        updates["$push"] = {"goals_completed": goals}
    if duration_hours is not None:
        print("time update")
        updates["duration_hours"] = duration_hours
    print("update")
    result = usetable.update_one(
          {"_id": ObjectId(studyID), "user_id": ObjectId(userID)},  
            {"$set": updates} if "$push" not in updates else updates 
     )
    return None 
    