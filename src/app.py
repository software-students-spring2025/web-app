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
    # the return value is sent as the response to the web browser
    return response

if __name__ == '__main__':
    PORT = os.getenv('PORT')
    app.run(port=(PORT or 3000))
