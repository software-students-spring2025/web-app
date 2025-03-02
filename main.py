import pymongo
from bson.objectid import ObjectId
import datetime

from dotenv import load_dotenv
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

##########################################################
# following is the original code
# can be deleted after finishing set up

# load_dotenv()

# MONGO_DBNAME = os.getenv('MONGO_DBNAME')
# MONGO_URI = os.getenv('MONGO_URI')
# client = pymongo.MongoClient(MONGO_URI)

# # Debuggings
# if not MONGO_URI:
#     raise ValueError("MONGO_URI is missing! Check your .env file.")

# db = client["test-database"]

# collection = db.test_collection

# # doc = {
# #     "name": "Foo Barstein",
# #     "email": "fb1258@nyu.edu",
# #     "message": "We loved with a love that was more than love.\n -Edgar Allen Poe",
# #     "created_at": datetime.datetime.utcnow() # the date time now
# # }

# # mongoid = collection.insert_one(doc)

# docs = collection.find({
#     "email": "fb1258@nyu.edu"
# })
# for doc in docs:
#     # print(doc)
#     output = '{name} ({email}) said "{message}" at {date}.'.format(
#         name = doc['name'],
#         email = doc['email'],
#         message = doc['message'],
#         date = doc['created_at'].strftime("%H:%M on %d %B %Y") # nicely-formatted datetime
#     )
#     print(output)