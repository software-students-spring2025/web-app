from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import os
import random
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

# create blueprint
quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/', methods = ['GET', 'POST'])
def quiz():
    session.setdefault('visited_quiz', True)
    session.setdefault('correct_count', 0)
    session.setdefault('wrong_count', 0)
    
    session['submitted'] = False 
        
    if request.method == 'POST' and 'next_question' in request.form or 'current_question' not in session:
        all_questions = list(questions_collection.find({}, {"_id": 0}))
        session['current_question'] = random.choice(all_questions) if all_questions else None
    
    total_questions = session['correct_count'] + session['wrong_count']
    
    return render_template('quiz.html', question = session['current_question'], correct_count = session['correct_count'], wrong_count = session['wrong_count'], total_questions = total_questions, submitted = session['submitted'])

@quiz_bp.route('/check_answer', methods = ['POST'])
def check_answer():
    user_answer = request.form.get('user_answer','').strip().lower()
    correct_answer = session.get('current_question', {}).get('answer', '').strip().lower()
    session.setdefault('submitted', False)
    result = ""
    
    if not session['submitted']:
        if user_answer == correct_answer:
            session['correct_count'] += 1
            result = f"Your answer is: {user_answer}<br>Correct!"
        else:
            session['wrong_count'] += 1
            result = f"Your answer is: {user_answer}<br>Wrong! The correct answer is: {session['current_question']['answer']}"
        session['submitted'] = True
            
    total_questions = session['correct_count'] + session['wrong_count']
        
    return render_template('quiz.html', question = session['current_question'], result = result, correct_count = session['correct_count'], wrong_count = session['wrong_count'], total_questions = total_questions, submitted = session['submitted'])