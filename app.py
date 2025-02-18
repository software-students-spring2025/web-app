from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# default landing page: login 
@app.route("/")
def index():
    return render_template("login.html")

# add dream page
@app.route("/add_dream", methods=["GET", "POST"])
def add_dream():
    return render_template("add_dream.html")