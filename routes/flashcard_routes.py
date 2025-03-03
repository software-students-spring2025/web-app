from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]
questions_collection = db.questions

# for debuggings
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing! Check your .env file.")

flashcard_bp = Blueprint('flashcard', __name__)

# NEW: Options route to allow the user to choose the flashcard order.
@flashcard_bp.route('/options', methods=['GET'])
def flashcard_options():
    return render_template('flashcard_options.html')  # Create flashcard_options.html accordingly


@flashcard_bp.route('/flashcard', methods=['GET'])

def flashcard():
    """
    Renders a flashcard page.
    
    This endpoint retrieves all questions from the database,
    and then uses a query parameter 'index' to select which question to display.
    """
    # Retrieve all questions as a list
    questions = list(questions_collection.find({}))
    total = len(questions)
    
    # If no questions are available, notify the user and redirect to add questions
    if total == 0:
        flash('No questions available for flashcards! Please add some questions first.', 'error')
        return redirect(url_for('questions.add_question'))
    
    # ADDED for shuffle option : Get the shuffle option from the query parameters (default is 'false')
    shuffle_option = request.args.get('shuffle', 'false')

    # Get the current flashcard index from the query parameters; default to 0
    try:
        index = int(request.args.get('index', 0))
    except ValueError:
        index = 0

    # Ensure index is within bounds
    if index < 0:
        index = 0
    if index >= total:
        index = total - 1
    if shuffle_option.lower() == "true":
        # Check if a shuffled order is already in the session
        if 'flashcard_order' not in session or len(session['flashcard_order']) != total:
            # Create a list of indices and shuffle it
            order = list(range(total))
            random.shuffle(order)
            session['flashcard_order'] = order
        else:
            order = session['flashcard_order']
        # Use the shuffled order to get the actual question index
        actual_index = order[index]
        question = questions[actual_index]
    else:
        # In sequential mode, use the index as-is
        question=questions[index]


    # Render the flashcard template, passing the current question,
    # the current index, and the total number of questions
    return render_template('flashcard.html', question=question, index=index, total=total, shuffle=shuffle_option)



# @flashcard_bp.route('/')
# def index():
#    return render_template('flashcard.html')