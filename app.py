from flask import Flask, render_template, request
from database import get_tasks

app = Flask(__name__)

# Home route - displays all tasks (Team Member 1)
@app.route('/')
def home():
    tasks = get_tasks()  # Retrieves all tasks from the database
    return render_template('index.html', tasks=tasks)

# Search route - filters tasks based on a keyword
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
