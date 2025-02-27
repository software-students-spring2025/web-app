from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
assert CONNECTION_STRING
DATABASE_NAME = os.environ.get("DATABASE_NAME")
assert DATABASE_NAME

connection = pymongo.MongoClient(CONNECTION_STRING)
print(connection)

db = connection[DATABASE_NAME]
print(db)

app = Flask(__name__)

@app.route('/')
def show_home():
    response = make_response("Home", 200)
    response.mimetype = "text/plain"
    return response