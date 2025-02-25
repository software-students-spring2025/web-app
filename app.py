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
if not uri:
    raise ValueError("MONGO_CONNECTION is not set in the .env file")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
#acess database
#create DB/Acess
myDb= client["DuoProject"]
#create table
myTable= myDb["users"]
ClassTable= myDb["Class"]
DeadlineTable= myDb["Deadlines"]
ExamsTable= myDb["Exams"]
StudiesTable= myDb["Studies"]
AssigmentsTable= myDb["Assigments"]
usid= "67bb780f0d9f7692fdfa4214"
object_id= ObjectId(usid)
#J =myTable.find_one({"username":"John"}) 
C= ClassTable.find_one({"user_ID":object_id})
doc = {
    "Class_Name":C["Class_Name"],
    "user_ID" : C["user_ID"],
    "Homwork1":"Math Homework",
    "Homework2":"Science",
    "H1_Due_Date": "Monday",
    "H2_Due_Date":"Friday"
}

upClass= AssigmentsTable.insert_one(doc)


#update user ID
#J =myTable.find_one({"username":"John"}) 
#StudiesTable.update_one(
#    
#    {"user_id":"123"},
#    {
#        "$set":{
#            "user_id": doc["user_ID"]
#        }
#    }
#)
print(client.list_database_names())
#Send a ping to confirm a successful connection
#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)