from flask import Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]
questions_collection = db.questions

# for debuggings
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing! Check your .env file.")

# Create Blueprint
questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form.get('question')
        answer_text = request.form.get('answer')
        hint_text = request.form.get('hint')
        difficulty_level = request.form.get('difficulty')

        if not question_text or not answer_text:
            return redirect(url_for('questions.add_question'))

        # Insert into MongoDB
        question = {
            "question": question_text,
            "answer": answer_text,
            "hint": hint_text,
            "difficulty": difficulty_level
        }
        questions_collection.insert_one(question)

        return redirect(url_for('questions.add_question'))

    return render_template('add_question.html')

@questions_bp.route('/show', methods = ['GET'])
def show_question():
    questions_to_show = questions_collection.find({})
    return render_template('questions.html', questions = questions_to_show)

@questions_bp.route('/delete', methods = ['GET', 'POST'])
def delete():
    questions_to_show = questions_collection.find({})
    if request.method == 'POST':
        to_delete = request.form.getlist('selected')
        print("to_delete",to_delete)
        if len(to_delete) == 0:
            flash("Please select something to delete!", "error")
            return redirect(url_for('questions.delete'))
        delete_count = 0

        for question_id in to_delete:
            delete_result = questions_collection.delete_one({"_id":  ObjectId(question_id)})
            if delete_result.deleted_count == 1:
                flash("Successfully deleted!", "success")
            else:
                flash("Unable to delete: Object no longer exist!", "error")
                
        return redirect(url_for('questions.delete'))

    return render_template('question_delete.html', questions = questions_to_show)