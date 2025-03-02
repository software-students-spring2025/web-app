import pymongo
from flask import Flask, redirect, render_template, request, url_for
from bson.objectid import ObjectId

app = Flask(__name__)

# make a connection to the database server
# do we leave it like this or hardcode it for our own?
connection = pymongo.MongoClient("mongodb://your_username:your_username@your_host_name:27017") 

db = connection["Forum"]    

# with data from database
@app.route("/")
def index2():
    posts = db.posts.find()
    return render_template("index.html", data=posts)

# with database
@app.route("/post/<int:post_id>")
def post_detail2(post_id):
    # Find the post by ID
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post:
        return render_template("post.html", post=post)
    else:
        return "<h1>Post Not Found</h1>", 404

if __name__ == "__main__":
    app.run(debug=True)



@app.route("/create_post", methods = ['GET','POST'])
def create_post2():

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

    result = db.posts.insert_one(new_post) # add post to database

    if result.inserted_id:
        # after making a post, where should user go?
        redirect(url_for(index2)) # this can change
    else:
        # check error code?
        return "<h1>Failed to add post</h1>", 404
    
    return render_template("create_post.html") # this actually shows the form to user i think

