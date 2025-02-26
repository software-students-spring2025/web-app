import db
import os
import config
import pymongo
from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)


@app.route('/')
def show_home():
    # put together an HTTP response with success code 200
    
    response = make_response("Welcome!", 200)
    # set the HTTP Content-type header to inform the browser that the returned document is plain text, not HTML
    response.mimetype = "text/plain"

    # Commented out MongoDB queries - these look correct:
    #tasks = list(db.tasks.find())
    #xp_counter = db.counters.find_one({"name": "xp_counter"})
    
    # Dummy values that should look like mongodb. 
    tasks = [
        {
            "_id": ObjectId(),
            "name": "1",
            "description": "1",
            "done_status": False,
            "xp_value": 50,
            "created_date": datetime.datetime.now() ,
            "due_date": datetime.datetime.now()
        },
        {
            "_id": ObjectId(),
            "name": "2",
            "description": "2",
            "done_status": False,
            "xp_value": 70,
            "created_date": datetime.datetime.now() ,
            "due_date": datetime.datetime.now()
        },
    ]
    
    xp_counter = 100  # some dummy value rn 
    
    
    return render_template('home.html', tasks=tasks, xp_counter=xp_counter)

#added in routes to other pages

@app.route('/edit')
def show_edit(): 
    return render_template('template/edit.html')

@app.route('/post')
def show_post(): 
    return render_template('template/post.html')

@app.route('/rec_del')
def show_rec_del(): 
    return render_template('template/rec_del.html')

@app.route('/search')
def show_search(): 
    return render_template('template/search.html')

@app.route('/search_results')
def show_search_results(): 
    return render_template('template/search_results.html')


if __name__ == '__main__':
    PORT = os.getenv('PORT')
    app.run(port=(PORT or 3000))
