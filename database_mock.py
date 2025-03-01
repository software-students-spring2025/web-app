from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template("index.html", data=mock_data)

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    # Find the post by ID
    post = next((item for item in mock_data if item["id"] == post_id), None)
    if post:
        return render_template("post.html", post=post)
    else:
        return "<h1>Post Not Found</h1>", 404

if __name__ == "__main__":
    app.run(debug=True)


# after run python database_mock.py in terminal, goto http://127.0.0.1:5000/ in browser
# this is just a mock backend to test if html works
# the routing can be used to the actual back end code (I believe) or you can make your own