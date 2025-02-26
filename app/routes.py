from flask import Blueprint, render_template

#create a Blueprint called main
main = Blueprint("main", __name__)

#defines '/' as the index.html html file
@main.route("/")
def home():
    return render_template("index.html")
