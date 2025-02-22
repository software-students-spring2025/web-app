from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv 
import os
import pymongo

#loading env file
load_dotenv()

#verify environmental variables
if not os.getenv("MONGO_URI") or not os.getenv("SECRET_KEY") or not os.getenv("MONGO_DBNAME"):
    raise ValueError("Missing required environment variable.")

#app setup
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

#mongodb setup
mongo = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo[os.getenv("MONGO_DBNAME")]

#verify mongodb connection
try:
    mongo.admin.command("ping")
    print("Connected to MongoDB")
except Exception as exception:
    print("MongoDB connection error:", exception)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()