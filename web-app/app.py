from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://testuser:testP@ssword@test-cluster.jeoj7.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = pymongo(app)

#mongoDB client
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]

#mongoDB client
#client = MongoClient('localhost', 27017)
#cxn = pymongo.MongoClient(os.getenv("mongodb+srv://testuser:testP@ssword@test-cluster.jeoj7.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster"))

sample_request = {
    "title": "Scandal",
    "season": 1,
    "episode": 2,
    "rating": 5,
    "comments": "Such an exciting start to the show!"
}

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return redirect(url_for('add'))

#add entry page
@app.route('/add', methods=['GET', 'POST'])
def add():
    #get data from HTML form
    if request.method == 'POST':
        show = request.form.get("show")
        season = request.form.get("season")
        episode = request.form.get("episode") 
        rating = request.form.get("rating") 
        comment = request.form.get("comment") 

        doc = {
            'title': show,
            'season': int(season or 0),
            'episode': int(episode or 0),
            'rating': int(rating or 0),
            'comment': comment
        }

        #insert data into user collection (may need to change, possibly inefficient for large num of users)
        db.user_entries.insert_one(doc)
        return redirect(url_for('success'))

    return render_template('add_show.html')

@app.route("/success")
def success():
    return "Data submitted successfully!"

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
