from flask import url_for, redirect, session, request
import os

from flask import Flask
from routes.questions_routes import questions_bp  # Import the questions Blueprint
from routes.quiz_routes import quiz_bp
from routes.flashcard_routes import flashcard_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Required for flash messages

# Register the questions Blueprints
app.register_blueprint(questions_bp, url_prefix='/question')
app.register_blueprint(quiz_bp, url_prefix='/quiz')
app.register_blueprint(flashcard_bp, url_prefix='/flashcard')

@app.before_request
def reset_quiz_session():
    """
    Reset session['visited_quiz'] when navigating away from /quiz
    Used to reset statistics like total_question_answered
    """
    if request.path.startswith('/static/'):
        return
    
    session.setdefault('visited_quiz', False)
    
    if session['visited_quiz'] and not request.path.startswith('/quiz'):
        session['correct_count'] = 0
        session['wrong_count'] = 0
        session['visited_quiz'] = False
    
    if request.path.startswith('/quiz'):
        session['visited_quiz'] = True

@app.route('/')
def home():
    return redirect(url_for("questions.show_question"))

if __name__ == '__main__':
    app.run(debug=True)