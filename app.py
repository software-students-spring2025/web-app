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

#Currently just prints "Home" to show app working, needs to acces task collection of DB and display tasks on template (HTML)
@app.route('/')
def show_home():
    response = make_response("Home", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    due = request.form.get("due")
    description = request.form.get("description")
    if task_name and due:
        task = {
            "name": task_name,
            "completed": False,
            "due_date": due,
            "description": description,
            "created_time": datetime.datetime.now()
        }
        tasks_collection.insert_one(task)
    return redirect(url_for('show_home'))

#Possible TODO: Implement a collection in the DB to store deleted tasks so they can be reinstated (or some other way to do it)
@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for('show_home'))

#Just add code to set completed from False to True, it could delete it after or something else visually up to you
@app.route('/complete/<task_id>')
def complete_task(task_id):
    #///////////
    return redirect(url_for('show_home'))

#forms that will allow user to edit the name, description and due date.
@app.route('/edit/<task_id>', methods=['POST'])
def edit_task(task_id):
    #///////////
    return redirect(url_for('show_home'))
    
if __name__ == '__main__':
    app.run(debug=True)
