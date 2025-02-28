from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI')  
MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'default_db')
client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]
tasks_collection = db['tasks']


def get_tasks():

    """
    Retrieves all tasks from the database.
    Returns:
        list: A list of all task documents as dictionaries.
    """
    tasks = list(tasks_collection.find().sort("created_at", -1))
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string for compatibility
    return tasks


def add_task(task):
    """
    Adds a new task to the database.
    Args:
        task (dict): A dictionary containing task details ('title', 'description', 'status').
    Returns:
        str: The ID of the inserted task.
    """
    task['created_at'] = datetime.utcnow()  # Add creation timestamp
    result = tasks_collection.insert_one(task)
    return str(result.inserted_id)


def update_task(task_id, title=None, description=None, status=None):
    """
    Updates an existing task in the database.
    Args:
        task_id (str): The ID of the task to update.
        title (str, optional): The new title of the task.
        description (str, optional): The new details of the task.
        status (str, optional): The new status of the task.
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    updated_data = {}
    if title:
        updated_data['title'] = title
    if description:
        updated_data['description'] = description
    if status:
        updated_data['status'] = status

    if updated_data:
        result = tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': updated_data}
        )
        return result.modified_count > 0
    return False


def delete_task(task_id):
    """
    Deletes a task from the database by ID.
    Args:
        task_id (str): The ID of the task to delete.
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return result.deleted_count > 0


def search_tasks(query):
    """
    Searches for tasks by title or description.
    Args:
        query (str): The search keyword.
    Returns:
        list: A list of matching task documents.
    """
    search_results = tasks_collection.find({
        '$or': [
            {'title': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}}
        ]
    }).sort("created_at", -1)

    tasks = list(search_results)
    for task in tasks:
        task['_id'] = str(task['_id'])
    return tasks


