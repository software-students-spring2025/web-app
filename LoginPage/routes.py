from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from bson.objectid import ObjectId
from app import app, mongo, bcrypt, login_manager
from models import User 


#Test/verify connection to database:  
@app.route('/test_db')
def test_db():
    try:
        collections = mongo.db.list_collection_names()
        return f"Connected to MongoDB! Collections: {collections}"
    except Exception as e:
        return f"Database connection error: {str(e)}"





@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login session"""
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None 

@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_user(username) #fetch from user collection
        if user and bcrypt.check_password_hash(user.password, password): 
            
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html') 


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #if account exists
        if mongo.db.users.find_one({"username": username}):
            flash("Username already exists!", "danger") 

        #hash the password and store it in a mongoDB database 
        else:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            #insert user as a new query
            mongo.db.users.insert_one({"username": username, "password": hashed_pw}) 

            #send messag showing account successfully made
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        
    #renders and returns HTML page to user's browser
    return render_template('register.html') 

@app.route('/home')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))