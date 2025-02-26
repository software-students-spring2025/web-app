from flask import Flask, jsonify, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['movie_db']
movies_collection = db['movies']

@app.route('/')
def index():
    return render_template('index.html')

# Edit to make specific to our app and add other features
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # Perform MongoDB search (case insensitive search example)
        results = movies_collection.find({"title": {"$regex": query, "$options": "i"}})
        movies = [{"title": movie['title'], "year": movie['year'], "synopsis": movie.get('synopsis', '')} for movie in results]
        return render_template('index.html', movies=movies)
    return render_template('index.html', movies=[])

def delete():
    if request.method == 'POST':
        # Get the show_id from the form
        show_id = request.form['show_id']
        
        # Try to delete the movie from the database
        result = movies_collection.delete_one({"_id": ObjectId(show_id)})
        
        # Check if deletion was successful
        if result.deleted_count > 0:
            message = "Show deleted successfully!"
        else:
            message = "Show not found or could not be deleted."

        # Fetch updated list of shows after deletion
        shows = movies_collection.find()
        return render_template('delete.html', shows=shows, message=message)

    # If it's a GET request, display the current watched list
    shows = movies_collection.find()
    return render_template('delete.html', shows=shows)

if __name__ == '__main__':
    app.run(debug=True)
