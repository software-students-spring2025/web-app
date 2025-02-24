from flask import Flask, render_template, request, url_for, redirect 
import pymongo
from bson.objectid import ObjectId
'''
notes / instructions

run app.py, then go to 127.0.0.1:5000 in browser

'''


# start app
app = Flask(__name__)

# clear leftover cookie(s) ?? May not be possible or necessary
# if user terminates this program WITHOUT manually logging out of their account, the cookie will remain in the browser and they will be automatically logged in when the app restarts

# connect MongoDB
# comment out if you don't have mongo yet, should still be fine 
client = pymongo.MongoClient('localhost', 27017)

'''
# this is the MOST simplified working app
# homepage
@app.route("/", methods=('GET', 'POST'))
def dashboard():
    if request.method == "GET":   
        return render_template('dashboard.html') # render home page template 
    return render_template('dashboard.html') # render home page template

# login
@app.route("/login", methods=('GET', 'POST'))
def show_login():
    if request.method == "GET":   
        return render_template('index.html') # render login page template 
    elif request.method == "POST":
        # not real support for posting, just a simple redirect
        response = redirect(url_for('dashboard'))
        #response.set_cookie('uid', request.form['uname'])
        return response
'''


# below shows basic implementation of "real" workflow - goes to homepage, checks if you're signed in, redirect to login if not
# will depend on things like 1) what you name form elements 2) what we want to use as a cookie, etc

# homepage / dashboard
@app.route("/", methods=('GET', 'POST'))
def show_dashboard():
    # show the dashboard
    if request.method == "GET":   
        print('cookies', request.cookies)
        # if we are logged in (uid cookie has been set) - load the dashboard page
        if 'uid' in request.cookies:
            print(request.cookies['uid'])
            return render_template('dashboard.html') # render home page template 
        # if we are NOT logged in - redirect to login
        return redirect(url_for('show_login'))
    # form handling
    elif request.method == "POST":
        pass  

    
    return render_template('dashboard.html') # render home page template 

# login
@app.route("/login", methods=('GET', 'POST'))
def show_login():
    # simply show the blank login page
    if request.method == "GET":   
        return render_template('signin.html') # render home page template 
    
    # if information has been submitted to login: 
    elif request.method == "POST":
        uname = request.form['username']
        ## 
        ## authenticate the username and password
        ##

        # set the uid cookie as the value of the user id
        # redirect to the dashboard
        response = redirect(url_for('show_dashboard'))
        response.set_cookie('uid', uname)
        return response
    
# sign up / new account
@app.route("/signup", methods=("GET", "POST"))
def show_signup():
    # simply show the blank signup page
    if request.method == "GET":   
        return render_template('signup.html') # render home page template 
    
    # if information has been submitted to signup: 
    elif request.method == "POST":
        print('form', request.form)
        ## 
        ## authenticate the username and password, create new user in mongo
        ##

        # set the uid cookie as the value of the user id
        # redirect to the dashboard
        response = redirect(url_for('show_dashboard'))
        response.set_cookie('uid', request.form['uname'])
        return response

# profile
@app.route("/profile", methods=("GET", "POST"))
def show_profile():
    # simply show the profile page
    if request.method == "GET":   
        return render_template('profile.html') # render home page template 
    
    # if user has clicked "sign out": clear session cookies and redirect to login page
    elif request.method == "POST":
        # DELETE the uid cookie 
        # redirect to the login page
        response = redirect(url_for('show_login'))
        response.delete_cookie("uid")
        return response




# keep alive
if __name__ == "__main__":
    app.run(debug=True) #running your server on development mode, setting debug to True
