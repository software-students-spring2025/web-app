import pymongo
import os
from flask import Flask, redirect, render_template, request, url_for
from bson.objectid import ObjectId
from dotenv import load_dotenv


app = Flask(__name__)

# make a connection to the database server

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

connection = pymongo.MongoClient(mongo_uri)
db = connection["Forum"]

# with data from database
@app.route("/")
def index():
    posts = db["posts"].find() 
    return render_template("index.html", data=posts)

# with database
@app.route("/post/<string:post_id>")
def post_detail(post_id):
    # Find the post by ID
    post = db["posts"].find_one({"_id": ObjectId(post_id)})
    if post:
        return render_template("post.html", post=post)
    else:
        return "<h1>Post Not Found</h1>", 404


@app.route("/create_post", methods = ['GET','POST'])
def create_post():

    user = None
    title = None
    content = None
    
    if request.method == "POST":
        # form fields the user fills out
        user = request.form.get("user")
        title = request.form.get("title")
        content = request.form.get("content")

        new_post = {
            "user": user,
            "title": title,
            "content": content,
            "comment": [] # new post will have no comments
        }

        result = db["posts"].insert_one(new_post) # add post to database

        if result.inserted_id: # check it was inserted
            # after making a post, where should user go?
            return redirect(url_for('index')) # this can change
        else:
            # check error code?
            return "<h1>Failed to add post</h1>", 404
    
    return render_template("create_post.html") 

@app.route("/post/<string:post_id>/comment", methods = ['POST'])
def add_comment(post_id):
    new_comment = { # idk if this should be form -- is this gonna be added to post detail page?
        "user": request.form.get("user"),
        "comment": request.form.get("content")
    }

    db["posts"].update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comment": new_comment}}
    )

    return redirect(url_for('post_detail', post_id=post_id))

@app.route("/post/<string:post_id>/edit", methods=['GET','POST'])
def edit_post(post_id):
    post = db["posts"].find_one({"_id": ObjectId(post_id)}) #find post (for get)

    if request.method == 'POST':
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        result = db["posts"].update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {
                "title": new_title,
                "content": new_content
            }}
        )

        if result.modified_count >= 1:
            return redirect(url_for('post_detail', post_id=post_id))
        else:
            return "<h1>Failed to edit post</h1>", 404
        
    return render_template("edit_post.html", post=post)


@app.route("/post/<string:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    db["posts"].delete_one({"_id": ObjectId(post_id)}) #delete post (for get)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)