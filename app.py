from flask import Flask, render_template
from dotenv import load_dotenv
import flask_login
import os
import pymongo
from bson.objectid import ObjectId
import datetime

load_dotenv()

connection = pymongo.MongoClient(os.getenv("MONGODB_URI"))

db = connection["testdb"]

app = Flask(__name__, template_folder='templates')

doc = {
    "test": ":3",
    "lol": "hi"
}

test = db.testdb.insert_one(doc)

@app.route('/')
def index():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5001), debug=False)