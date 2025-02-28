from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

mongo = PyMongo(app, uri=os.getenv("MONGO_URI"))
db = mongo.db

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": user_id})
    if user_data:
        return User(user_data["_id"], user_data["username"])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = db.users.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data["_id"], user_data["username"])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('add.html')
    title = request.form.get("title")
    description = request.form.get("description")
    status = "pending"
    task = {"title": title, "description": description, "status": status}
    add_task(task)
    return render_template('add.html', task=task)

@app.route('/update/<task_id>', methods=['GET', 'POST'])
@login_required
def update(task_id):
    task = next((t for t in get_tasks() if t["_id"] == task_id), None)
    if not task:
        return "Task not found", 404

    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")

        success = update_task(task_id, title, description, status)
        if success:
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Failed to update task {task_id}")
        return redirect(url_for('index'))
    return render_template('update.html', task=task)

@app.route('/delete/<task_id>', methods=['POST'])
@login_required
def delete(task_id):
    success = delete_task(task_id)
    if success:
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Failed to delete task {task_id}.")
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').lower()
    tasks = get_tasks()
    filtered_tasks = []
    if query:
        filtered_tasks = [
            task for task in tasks
            if query in task.get('title', '').lower() or query in task.get('description', '').lower()
        ]
    return render_template('search.html', tasks=filtered_tasks)

@app.route('/completed')
@login_required
def completed():
    tasks = get_tasks()
    completed_tasks = [task for task in tasks if task.get('status') == 'completed']
    return render_template('completed.html', tasks=completed_tasks)

def get_tasks():
    return list(db.tasks.find())

def add_task(task):
    db.tasks.insert_one(task)

def update_task(task_id, title, description, status):
    result = db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"title": title, "description": description, "status": status}}
    )
    return result.modified_count > 0

def delete_task(task_id):
    result = db.tasks.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0

if __name__ == '__main__':
    app.run(debug=True)