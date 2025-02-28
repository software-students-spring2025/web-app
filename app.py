from flask import Flask, render_template, request
from database import get_tasks, add_task, delete_task
from bson.objectid import ObjectId

app = Flask(__name__)

# Home route - displays all tasks 
@app.route('/')
def home():
    tasks = get_tasks()  # Retrieves all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/add',methods=['POST','GET'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    title=request.form.get("title")
    description=request.form.get("description")
    status="pending"
    task = {"title":title,"description":description,"status":status}
    add_task(task)
    return render_template('add.html', task=task)

@app.route('/delete/<task_id>',methods=['POST'])
def delete(task_id):
    success = delete_task(task_id)
    if success:
        print(f"Task {task_id} deleted successfully")
    else: 
        print(f"Failed to delete task {task_id}.")
    tasks = get_tasks()  # Retrieves all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()  # Retrieve the search keyword
    tasks = get_tasks()  
    filtered_tasks = []
    if query:
        # Filter tasks by query
        filtered_tasks = [
            task for task in tasks
            if query in task.get('title', '').lower() or query in task.get('description', '').lower()
        ]
    return render_template('search.html', tasks=filtered_tasks)

# Completed tasks route - shows 'completed' tasks
@app.route('/completed')
def completed():
    tasks = get_tasks()
    # Filter tasks with status 'completed'
    completed_tasks = [task for task in tasks if task.get('status') == 'completed']
    return render_template('completed.html', tasks=completed_tasks)

if __name__ == '__main__':
    app.run(debug=True)
