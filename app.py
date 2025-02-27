from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["movie_tracker"]
movies_collection = db["movies"]

# User Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({"username": username, "password": hashed_password})
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({"username": username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

#add movie route - check to see if links correctly Jime 
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
   ## if 'user_id' not in session:
       ## return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        release_year = request.form['release_year']
        
        
        movies_collection.insert_one({

            "title": title,
            "genre": genre,
            "release_year": release_year
        })
        
        flash('Movie added successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to home instead of dashboard
    
    return render_template('add.html')


#edit movie route -- check to see if links correclty Jime
@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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