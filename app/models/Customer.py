from pymongo import MongoClient

# prevent circular imports
def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client.my_database

'''

Customers should be able to make, edit, delete orders,
View menu,
Send contact messages to employees
Submit name, email address, address, and credit card info

'''

class Customer:
    def create_customer():
        pass