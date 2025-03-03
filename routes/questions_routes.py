from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
        genre_text = request.form.get('genre')

        if not question_text or not answer_text:
            return redirect(url_for('questions.add_question'))

        # Insert into MongoDB
        question = {
            "question": question_text,
            "answer": answer_text,
            "hint": hint_text,
            "difficulty": difficulty_level,
            "genre" : genre_text,
            "bookmarked": False
        }
        questions_collection.insert_one(question)

        return redirect(url_for('questions.add_question'))

    return render_template('add_question.html')

@questions_bp.route('/show', methods = ['GET', 'POST'])
def show_question():
    genres = [g for g in questions_collection.distinct("genre") if g and g.strip()]
    difficulties = [d for d in questions_collection.distinct("difficulty") if d and d.strip()]
    
    selected_genre = request.form.get('genre', '')
    selected_difficulty = request.form.get('difficulty', '')
    bookmarked_filter = request.form.get('bookmarked', '') == 'true'
    
    query = {}
    if selected_genre:
        query["genre"] = selected_genre
    if selected_difficulty:
        query["difficulty"] = selected_difficulty
    if bookmarked_filter:
        query["bookmarked"] = True
    
    questions_to_show = list(questions_collection.find(query))
    for question in questions_to_show:
        question['_id'] = str(question['_id'])
    
    if request.method == 'POST':
        if 'start_quiz' in request.form or 'start_flashcards' in request.form:
            selected_questions = request.form.getlist('selected')
            if not selected_questions:
                flash("Please select at least one question!", "error")
                return redirect(url_for('questions.show_question'))

            session['selected_questions'] = selected_questions

            if 'start_quiz' in request.form:
                return redirect(url_for('quiz.quiz'))
            elif 'start_flashcards' in request.form:
                return redirect(url_for('flashcard.flashcard_options'))

    return render_template('questions.html', 
                           questions = questions_to_show, 
                           genres = genres, 
                           difficulties = difficulties, 
                           selected_genre = selected_genre, 
                           selected_difficulty = selected_difficulty)

@questions_bp.route('/delete', methods = ['GET', 'POST'])
def delete():
    """Delete a question using checkbox"""
    questions_to_show = questions_collection.find({})
    if request.method == 'POST':
        to_delete = request.form.getlist('selected')
        print("to_delete",to_delete)
        if len(to_delete) == 0:
            flash("Please select something to delete!", "error")
            return redirect(url_for('questions.delete'))

        for question_id in to_delete:
            delete_result = questions_collection.delete_one({"_id":  ObjectId(question_id)})
            if delete_result.deleted_count == 1:
                flash("Successfully deleted!", "success")
            else:
                flash("Unable to delete: Object no longer exist!", "error")
                
        return redirect(url_for('questions.delete'))

    return render_template('question_delete.html', questions = questions_to_show)

@questions_bp.route('/search', methods = ['GET', 'POST'])
def search():
    """ 
    Searching through questions.
    Using an "and" logic to search through the database.
    Using "regex" to search inside a string -- no strict match needed.
    Change to "^...$" if strict match is needed.
    Case-insensitive.
    """
    questions_to_show = questions_collection.find({})
    if request.method == 'POST':
        question_text    = request.form.get( 'question'   )
        answer_text      = request.form.get( 'answer'     )
        hint_text        = request.form.get( 'hint'       )
        difficulty_level = request.form.get( 'difficulty' )
        genre            = request.form.get( 'genre'      )

        questions_to_show = questions_collection.find({
            '$and':[
                { "question"     : { "$regex" : question_text    , "$options": "i" }},
                { "answer"       : { "$regex" : answer_text      , "$options": "i" }},
                { "hint"         : { "$regex" : hint_text        , "$options": "i" }},
                { "difficulty"   : { "$regex" : difficulty_level , "$options": "i" }},
                { "genre"        : { "$regex" : genre            , "$options": "i" }},
            ]
        })
    return render_template('question_search.html', questions = questions_to_show)

@questions_bp.route('/edit/<q_id>', methods = ['GET', 'POST'])
def edit(q_id):
    """
    Edit Questions
    """
    print("editing question")
    print(q_id)
    question_to_show = questions_collection.find_one( { '_id': ObjectId(q_id) } )
    if question_to_show is None:
        print(q_id)
        flash("Question not found!", "error")
        return redirect(url_for("questions.show_question"))
    if request.method == 'POST':
        question_text    = request.form.get( 'question'   )
        answer_text      = request.form.get( 'answer'     )
        hint_text        = request.form.get( 'hint'       )
        difficulty_level = request.form.get( 'difficulty' )
        genre            = request.form.get( 'genre'      )
        newvalues = {
            "$set": { 
                "question"     : question_text,
                "answer"       : answer_text,
                "hint"         : hint_text,
                "difficulty"   : difficulty_level,
                "genre"        : genre,
            }
        }
        questions_collection.update_one(
            {'_id': ObjectId(q_id)},
            newvalues
            )
        return redirect(url_for("questions.show_question"))
    return render_template("question_edit.html", question = question_to_show)

@questions_bp.route('/toggle_bookmark/<q_id>', methods=['GET'])
def toggle_bookmark(q_id):
    question = questions_collection.find_one({"_id": ObjectId(q_id)})
    
    new_bookmarked_status = not question.get("bookmarked", False)
    questions_collection.update_one(
        {"_id": ObjectId(q_id)},
        {"$set": {"bookmarked": new_bookmarked_status}}
    )

    return redirect(request.referrer or url_for("questions.show_question"))
