from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)

@app.route('/')
def show_home():
    response = make_response("Home", 200)
    response.mimetype = "text/plain"
    return response