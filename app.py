import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file


app = Flask(__name__)
            
config = dotenv_values()
app.config.from_mapping(config)

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]

try:
    cxn.admin.command("ping")
    print(" *", "Connected to MongoDB!")
except Exception as e:
    print(" * MongoDB connection error:", e)


@app.route("/")
def home():
    """
    Route for the home page with all available courses and a button to add a new course.
    Returns:
        rendered template (str): The rendered HTML template.
    """
    courses = db.courses.find().sort("created_at", -1)
    return render_template("home.html", docs=courses)


@app.route("/course/<course_id>")
def course(course_id):
    """
    Route for the course page with the course details and a link to see the course roaster.
    Returns:
        rendered template (str): The rendered HTML template.
    """
    return render_template("course.html")

@app.route("/course/<course_id>/roaster")
def course_roaster(course_id):
    """
    Route for the course roaster page with an option to search for specific student and see their grades.
    Returns:
        rendered template (str): The rendered HTML template.
    """
    return render_template("course_roaster.html")

@app.route("/course/<course_id>/student_grades/<student_id>")
def studnet_grades(course_id, student_id):
    """
    Route for the course roaster page.
    Returns:
        rendered template (str): The rendered HTML template.
    """
    return render_template("course_student.html")

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
