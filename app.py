from flask import Flask, render_template, request, redirect, url_for, flash, session
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
# import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient("mongodb+srv://sms10010:Wittmer2@swe-project2.zdloe.mongodb.net/?retryWrites=true&w=majority&appName=SWE-project2",tlsCAFile=certifi.where())
db = client["movie_tracker"]
movies_collection = db["movies"]
users_collection = db["users"]


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    username = session['username'] 
    user = movies_collection.find_one({"username": username})
    movies = user.get("movies", []) if user else []

    return render_template('home.html', movies=movies)

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})

        # Check if user exists and if the password matches
        if user and user['password'] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if users_collection.find_one({"username": username}):
            flash("Username already exists. Please choose a different one.")
        else:
            users_collection.insert_one({
                "username": username,
                "password": password,
            })

            movies_collection.insert_one({
                "username": username, 
                "movies": []
            })
            
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
    return render_template('register.html')


# add movie route - check to see if links correctly Jime





@app.route("/add", methods=["GET", "POST"])

def add_movie():

    username = session['username']

    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        release_year = request.form.get("release_year")

        if title and genre and release_year:
            new_movie = {
                "title": title,
                "genre": genre,
                "release_year": release_year
            }

            movies_collection.update_one(
                {"username": username},
                {"$push": {"movies": new_movie}}
            )

        return redirect(url_for('home'))

    return render_template("add.html")

#movie details
@app.route('/movie_details/<username>/<title>', methods=['GET'])
def movie_details(username, title):
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure the user is logged in

    # Find the user's movie list by username
    user_movies = movies_collection.find_one({"username": username})

    # If the user exists and has movies
    if user_movies and 'movies' in user_movies:
        # Find the movie by its title in the movies array
        movie = next((m for m in user_movies['movies'] if m['title'] == title), None)

        if movie:
            # Movie found, pass details to the template
            return render_template('details.html', movie=movie)
        else:
            flash("Movie not found!")
            return redirect(url_for('home'))
    else:
        flash("No movies found for this user!")
        return redirect(url_for('home'))



# edit movie route -- check to see if links correclty Jime
@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        release_year = request.form['release_year']

        movies_collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": {"title": title, "genre": genre, "release_year": release_year}}
        )

        flash('Movie updated successfully!', 'success')
        return redirect(url_for('movie_details', movie_id=movie_id))

    return render_template('edit.html', movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
