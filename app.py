from pymongo import MongoClient
import os

# This function serves to get access and retrieve necessaary data from MongoDB which we will use throughout the application
def get_database():
   CONNECTION_STRING = os.environ['MONGO_CONNECTION']

   if (CONNECTION_STRING):
        client = MongoClient(CONNECTION_STRING)

        if (client):
            return client['name of database']
        else:
            return("Err: Could not make connection with database, please check Connection String!")
        
   else:
       return("Err: Connection string is incorrect or invalid!")
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   name_of_database = get_database()