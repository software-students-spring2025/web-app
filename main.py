import os

from flask import Flask
from routes.questions_routes import questions_bp  # Import the questions Blueprint

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Required for flash messages

# Register the questions Blueprints
app.register_blueprint(questions_bp, url_prefix='/question')

@app.route('/')
def home():
    return '''
    Welcome to the Quiz App! <a href='/question/add'>Add Question</a>
    <a href='/question/show'>Show Question</a>
    '''
if __name__ == '__main__':
    app.run(debug=True)