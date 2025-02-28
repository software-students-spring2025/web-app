from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
import os
import pymongo
from bson.objectid import ObjectId
import datetime

load_dotenv()
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
assert CONNECTION_STRING
DATABASE_NAME = os.environ.get("DATABASE_NAME")
assert DATABASE_NAME

connection = pymongo.MongoClient(CONNECTION_STRING)
#print(connection)

db = connection[DATABASE_NAME]
#print(db)

tasks_collection = db["tasks"]

app = Flask(__name__)

@app.route('/')
def show_home():
    response = make_response("Home", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/add', methods=['POST'])
def add_task():
    #///////////
    return redirect(url_for('show_home'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    #///////////
    return redirect(url_for('show_home'))

@app.route('/complete/<task_id>')
def complete_task(task_id):
    #///////////
    return redirect(url_for('show_home'))

@app.route('/edit/<task_id>', methods=['POST'])
def edit_task(task_id):
    #///////////
    return redirect(url_for('show_home'))
    
if __name__ == '__main__':
    app.run(debug=True)
