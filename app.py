from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['movie_db']
movies_collection = db['movies']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # Perform MongoDB search (case insensitive search example)
        # Edit to make specific to our app
        results = movies_collection.find({"title": {"$regex": query, "$options": "i"}})
        movies = [{"title": movie['title'], "year": movie['year'], "synopsis": movie.get('synopsis', '')} for movie in results]
        return render_template('index.html', movies=movies)
    return render_template('index.html', movies=[])

if __name__ == '__main__':
    app.run(debug=True)
