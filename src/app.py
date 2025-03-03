import db
import os
import config
import pymongo
import datetime
import threading
import time
import functools
import operator
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)


@app.route('/')
def show_home():  
    # Dummy values that should look like mongodb. 
    # tasks = [
    #     {
    #         "_id": ObjectId(),
    #         "name": "1",
    #         "description": "1",
    #         "done_status": False,
    #         "xp_value": 50,
    #         "created_date": datetime.datetime.now() ,
    #         "due_date": datetime.datetime.now()
    #     },
    #     {
    #         "_id": ObjectId(),
    #         "name": "2",
    #         "description": "2",
    #         "done_status": False,
    #         "xp_value": 70,
    #         "created_date": datetime.datetime.now() ,
    #         "due_date": datetime.datetime.now()
    #     },
    # ]
    
    tasks = list(db.tasks.find())
    xp = functools.reduce(lambda acc, task: acc + task['xp_value'], tasks, 0)

    return render_template('home.html', tasks=tasks, xp=xp)

#added in routes to other pages

@app.route('/edit', methods=['GET','POST'])
def show_edit(): 
    #form to edit 
    if request.method == 'POST':
        task_id = request.form.get("task_id")

        db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {
                "name": request.form.get("name"),
                "description": request.form.get("done_status") == "true",
                "xp_value": int(request.form.get("xp_value")),
                "due_date": datetime.datetime.strptime(request.form.get("due_date"), "%Y-%m-%d")
            }}
        )
        #goes home for edit
        return redirect(url_for('show_home'))
    
    else:
        task_id = request.args.get("task_id")
        tasks = list(db.tasks.find())
        selected_task = None

        if task_id:
            selected_task = db.tasks.find_one({"_id": ObjectId(task_id)})
        
        return render_template('edit.html', tasks=tasks,selected_task=selected_task)

@app.route('/new_post', methods = ['POST'])
def create_new_post(): 
    completed = request.form.get("completed", "")
    if completed:
        done_status = True
    else:
        done_status = False
    newTask = {
            "_id": ObjectId(),
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip(),
            "done_status": done_status,
            "xp_value": int(request.form.get("xp", "").strip()),
            "created_date": datetime.datetime.now(),
            "due_date": datetime.datetime(
                int(request.form.get("year", "").strip()),
                int(request.form.get("month", "").strip()),
                int(request.form.get("day", "").strip())
            )
    }
    db.tasks.insert_one(newTask);
    return redirect(url_for('show_home'))

@app.route('/post')
def show_post(): 
    return render_template('post.html')

@app.route('/rec_del')
def show_rec_del(): 
    try:
        deleted_tasks = list(db.deleted_tasks.find())
        return render_template('rec_del.html', tasks=deleted_tasks)
    except Exception as e:
        return f"Error retrieving deleted tasks: {str(e)}", 500

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        task = db.tasks.find_one({"_id": ObjectId(task_id)})
        if task:
            task["deleted_at"] = datetime.datetime.now()
            db.deleted_tasks.insert_one(task)
            db.tasks.delete_one({"_id": ObjectId(task_id)})
        return redirect(url_for('show_home'))
    except Exception as e:
        return f"Error deleting task: {str(e)}", 500

def cleanup_old_deleted_tasks():
    while True:
        threshold_date = datetime.datetime.now() - datetime.timedelta(days=30)
        db.deleted_tasks.delete_many({"deleted_at": {"$lt": threshold_date}})
        time.sleep(86400)
#start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_deleted_tasks, daemon=True)
cleanup_thread.start()


@app.route('/search')
def show_search(): 
    
    return render_template('search.html')

@app.route('/search_results')
def show_search_results(): 
    query = request.args.get("search", "").strip()
    if query:
        search_filter = {
            "$or": [
                {"name": {"$regex": f".*{query}.*", "$options": "i"}},
                {"description": {"$regex": f".*{query}.*", "$options": "i"}}
            ]
        }
        tasks = list(db.tasks.find(search_filter))
    else:
        tasks = []
    return render_template('search_results.html', tasks=tasks, search_query=query)

#for debugging purposes only
''' 
@app.route('/test_db')
def test_db():
    try:
        print(f"Using database: {db.name}")  # Debugging
        test_task = db.tasks.find_one()
        if test_task:
            return f"Connected to MongoDB! Found a task: {test_task}"
        else:
            return "Connected to MongoDB, but no tasks found."
    except Exception as e:
        return f"Error connecting to MongoDB: {str(e)}"
'''
if __name__ == '__main__':
    PORT = os.getenv('PORT')
    app.run(port=(PORT or 3000))
