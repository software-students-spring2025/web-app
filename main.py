from flask import url_for, redirect
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

@app.route('/')
def home():
    return redirect(url_for("questions.show_question"))

if __name__ == '__main__':
    app.run(debug=True)