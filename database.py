import pymongo

# make a connection to the database server
# do we leave it like this or hardcode it for our own?
connection = pymongo.MongoClient("mongodb://your_username:your_username@your_host_name:27017") 

db = connection["Forum"]



