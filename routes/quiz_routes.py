from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import os
import random
from dotenv import load_dotenv
from bson.objectid import ObjectId

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
    session.setdefault('answered_questions', [])
    
    if request.referrer and '/show' in request.referrer:
        session['answered_questions'] = []
        session['submitted'] = False
    
    if 'selected_questions' in session and session['selected_questions']:
        selected_ids = [ObjectId(q_id) for q_id in session['selected_questions']]
        all_questions = list(questions_collection.find({"_id": {"$in": selected_ids}}))
    else:
        all_questions = []
    
    for q in all_questions:
        q['_id'] = str(q['_id'])
    
    unanswered_questions = [q for q in all_questions if q['_id'] not in session['answered_questions']]

    if unanswered_questions:
        session['current_question'] = random.choice(unanswered_questions)
        session['submitted'] = False
    else:
        session['current_question'] = None
    
    total_questions = session['correct_count'] + session['wrong_count']
    
    return render_template(
        'quiz.html',
        question=session['current_question'],
        correct_count=session['correct_count'],
        wrong_count=session['wrong_count'],
        total_questions=total_questions,
        submitted=session.get('submitted', False))
    
@quiz_bp.route('/check_answer', methods = ['POST'])
def check_answer():
    user_answer = request.form.get('user_answer','').strip().lower()
    correct_answer = session.get('current_question', {}).get('answer', '').strip().lower()
    session.setdefault('submitted', False)
    session.setdefault('answered_questions', [])
    result = ""
    
    if not session['submitted']:
        if user_answer == correct_answer:
            session['correct_count'] += 1
            result = f"Your answer is: {user_answer}<br>✅ Correct!"
        else:
            session['wrong_count'] += 1
            result = f"Your answer is: {user_answer}<br>❌ Wrong! The correct answer is: {session['current_question']['answer']}"
        session['submitted'] = True
        if 'current_question' in session and '_id' in session['current_question']:
            session['answered_questions'].append(session['current_question']['_id'])
   
    total_questions = session['correct_count'] + session['wrong_count']
        
    return render_template('quiz.html', 
                           question = session['current_question'],
                           result = result, 
                           correct_count = session['correct_count'], 
                           wrong_count = session['wrong_count'], 
                           total_questions = total_questions, 
                           submitted = session['submitted'])

@quiz_bp.route('/restart', methods=['POST'])
def restart_quiz():
    """Resets quiz progress and starts fresh"""
    session.pop('correct_count', None)
    session.pop('wrong_count', None)
    session.pop('answered_questions', None)
    session.pop('submitted', None)
    session['visited_quiz'] = False
    return redirect(url_for('quiz.quiz'))
