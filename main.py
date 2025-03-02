import pymongo
from bson.objectid import ObjectId
import datetime

from dotenv import load_dotenv
import os

from flask import Flask
from flask import render_template
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
    return render_template("questions.html")

if __name__ == '__main__':
    app.run(debug=True)