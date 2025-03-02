from flask import Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
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

@questions_bp.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form.get('question')
        answer_text = request.form.get('answer')
        hint_text = request.form.get('hint')
        difficulty_level = request.form.get('difficulty')

        if not question_text or not answer_text:
            flash("Please fill in all fields!", "error")
            return redirect(url_for('questions.add_question'))

        # Insert into MongoDB
        question = {
            "question": question_text,
            "answer": answer_text,
            "hint": hint_text,
            "difficulty": difficulty_level
        }
        questions_collection.insert_one(question)

        flash("Question added successfully!", "success")
        return redirect(url_for('questions.add_question'))

    return render_template('add_question.html')