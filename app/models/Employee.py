from pymongo import MongoClient

# prevent circular imports
def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client.my_database

'''

Employees should be able to view orders and change order statuses,
View customer messages,
Edit, add, and delete menu items,
Log in to employee view

'''

class Employee:
    def create_customer():
        pass