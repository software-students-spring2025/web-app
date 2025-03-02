from flask import Flask, redirect, render_template, url_for,request
from bson.objectid import ObjectId

mock_app = Flask(__name__)

# Updated mock data with structured sections
mock_data = [
    {
        "id": 1,
        "user": "Albert",
        "title": "Post 111",
        "content": "This is where the content gose, and Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer feugiat porttitor dui quis sollicitudin. Sed lorem felis, cursus nec sapien at, consectetur volutpat eros. ",
        "comment": ["Great post!", "Thanks for sharing.", "Very informative."]
    },
    {
        "id": 2,
        "user": "Bob",
        "title": "testing title",
        "content": "content gose here, and Phasellus vel ullamcorper nulla. Vivamus vitae tellus at lacus viverra tempor. Nunc in eros et risus mollis scelerisque eu a augue. ",
        "comment": ["Sounds fun!", "Nice story.", "Hope you had a good day!"]
    },
    {
        "id": 3,
        "user": "ChatABC",
        "title": "Title title title",
        "content": "here lyes the content, and Maecenas ut nunc libero. Duis non magna et urna mattis pharetra sit amet rhoncus sapien. Donec ullamcorper commodo tincidunt.",
        "comment": ["Interesting read.", "Fascinating!", "Looking forward to more updates."]
    }
]

# test with mock data
@mock_app.route("/")
def index():
    return render_template("index.html", data=mock_data)

# for testing
@mock_app.route("/post/<int:post_id>")
def post_detail(post_id):
    # Find the post by ID
    post = next((item for item in mock_data if item["id"] == post_id), None)
    if post:
        return render_template("post.html", post=post)
    else:
        return "<h1>Post Not Found</h1>", 404
    

# after run python database_mock.py in terminal, goto http://127.0.0.1:5000/ in browser
# this is just a mock backend to test if html works
# the routing can be used to the actual back end code (I believe) or you can make your own

@mock_app.route("/create_post", methods = ['GET','POST'])
def create_post():

    if request.method == "POST":
        # get data from user/form
        user = request.form.get("user")
        title = request.form.get("title")
        content = request.form.get("content")

        print(f"User: {user}, Title: {title}, Content: {content}")

        new_post = {
            "id": 4, # need to add this just for mock data
            "user": user,
            "title": title,
            "content": content,
            "comment": []  # new post has no comments initially
        }

        mock_data.append(new_post) # add post to mock_data
        return redirect(url_for('index')) # this can change

    # for if the request is get
    return render_template("create_post.html") # this actually shows the form to user i think



if __name__ == "__main__":
    mock_app.run(debug=True)