from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient('your_mongo_uri')
db = client.your_database_name

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user_data = db.users.find_one({"_id": user_id})
        if user_data:
            return User(user_data["_id"], user_data["username"], user_data["password"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.users.find_one({"username": username}):
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        new_user = {
            "username": username,
            "password": password
        }
        db.users.insert_one(new_user)
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = db.users.find_one({"username": username})
        if user_data and user_data["password"] == password:
            user = User(user_data["_id"], user_data["username"], user_data["password"])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db.tasks.insert_one({"title": title, "description": description, "status": "pending"})
        flash('Task added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.tasks.find_one({"_id": task_id})
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db.tasks.update_one({"_id": task_id}, {"$set": {"title": title, "description": description}})
        flash('Task updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<task_id>')
@login_required
def delete_task(task_id):
    db.tasks.delete_one({"_id": task_id})
    flash('Task deleted successfully!')
    return redirect(url_for('index'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    tasks = list(db.tasks.find({"title": {"$regex": query, "$options": "i"}}))
    return render_template('search.html', tasks=tasks)

@app.route('/completed')
@login_required
def completed_tasks():
    tasks = list(db.tasks.find({"status": "completed"}))
    return render_template('completed.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)