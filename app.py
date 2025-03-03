import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    UserMixin,
    current_user,
)
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
from flask import session


# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "yoursecretkey"

# Set up MongoDB connection using pymongo
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.get_database("jobtracker")
users_collection = db.get_collection("users")
applications_collection = db.get_collection("applications")

interview_collection = db.get_collection("interview_collection")

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

practice_questions = [
    {"difficulty": "Easy", "question_content": "Practice Question 1: ?????"},
    {"difficulty": "Medium", "question_content": "Practice Question 2: ?????"},
    {"difficulty": "Hard", "question_content": "Practice Question 3: ?????"}
]

mock_questions = [
    {"difficulty": "Medium", "question_content": "Mock Question 1: ?????"},
    {"difficulty": "Hard", "question_content": "Mock Question 2: ?????"},
    {"difficulty": "Hard", "question_content": "Mock Question 3: ?????"}
]

# Define a User class that integrates with Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = users_collection.find_one({"email": email})

        if user_data and check_password_hash(user_data["password"], password):
            user_obj = User(user_data)
            login_user(user_obj)
            flash("Logged in successfully", "success")
            return redirect(url_for("home"))  # Redirect clears the flash message

        else:
            flash("Invalid email or password", "danger")
    
    return render_template("login.html")  # Flash messages only shown after submission


# 注册
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("signup"))
        if users_collection.find_one({"email": email}):
            flash("Email already registered", "danger")
            return redirect(url_for("signup"))
        hashed_password = generate_password_hash(password)
        user_id = users_collection.insert_one(
            {"email": email, "password": hashed_password}
        ).inserted_id
        user_data = users_collection.find_one({"_id": user_id})
        user_obj = User(user_data)
        login_user(user_obj)
        flash("Account created and logged in", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")


# Home screen (protected route)
@app.route("/home", methods=["GET"])
@login_required
def home():
    search_query = request.args.get("search", "").strip()

    if search_query:
        applications = list(applications_collection.find({
            "$and": [
                {"user_id": current_user.id},
                {"$or": [
                    {"company": {"$regex": search_query, "$options": "i"}},
                    {"job_title": {"$regex": search_query, "$options": "i"}}
                ]}
            ]
        }))
    else:
        applications = list(applications_collection.find({"user_id": current_user.id}))
        
    total_apps = len(applications)
    interview_count = sum(1 for app in applications if app.get("status") == "Interview")
    offer_count = sum(1 for app in applications if app.get("status") == "Offered")

    return render_template(
        "home.html",
        applications=applications,
        user=current_user,
        total_apps=total_apps,
        interview_count=interview_count,
        offer_count=offer_count
    )

@app.route("/add_application", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        applications_collection.insert_one({
            "user_id": current_user.id,
            "company": company,
            "job_title": job_title,
            "status": status,
            "application_date": application_date,
            "note": note
        })

        flash("New application added!", "success")
        return redirect(url_for("home"))

    return render_template("add_application.html")

# 登出
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))


@app.route("/delete_application/<application_id>", methods=["GET"])
@login_required
def delete_application(application_id):
    applications_collection.delete_one({"_id": ObjectId(application_id)})
    flash("Application deleted successfully!", "success")
    return redirect(url_for("home"))

@app.route("/edit_application/<application_id>", methods=["GET", "POST"])
@login_required
def edit_application(application_id):
    application = applications_collection.find_one({"_id": ObjectId(application_id)})

    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        applications_collection.update_one(
            {"_id": ObjectId(application_id)},
            {"$set": {
                "company": company,
                "job_title": job_title,
                "status": status,
                "application_date": application_date,
                "note": note
            }}
        )
        flash("Application updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_application.html", application=application)
@app.route("/search_application", methods=["GET", "POST"])
@login_required
def search_application():
    if request.method == "POST":
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        status = request.form.get("status")
        application_date = request.form.get("application_date")
        note = request.form.get("note")

        # Build search query
        query = {"user_id": current_user.id}
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        if job_title:
            query["job_title"] = {"$regex": job_title, "$options": "i"}
        if status:
            query["status"] = {"$regex": status, "$options": "i"}
        if application_date:
            query["application_date"] = application_date
        if note:
            query["note"] = {"$regex": note, "$options": "i"}

        # Perform search in MongoDB
        search_results = list(applications_collection.find(query))

        return render_template("search_results.html", results=search_results)

    return render_template("search_application.html")

@app.route("/interview")
@login_required
def interview():
    return render_template("interview.html")

# Practice 筛选页面
@app.route("/interview/practice_filter", methods=["GET", "POST"])
@login_required
def practice_filter():
    if request.method == "POST":
        # 初始化 practice_answers
        session['practice_answers'] = {}
        return redirect(url_for("practice_question", index=0))
    return render_template("practice_filter.html")

# Mock 筛选页面
@app.route("/interview/mock_filter", methods=["GET", "POST"])
@login_required
def mock_filter():
    if request.method == "POST":
        # 初始化 mock_answers
        session['mock_answers'] = {}
        return redirect(url_for("mock_question", index=0))
    return render_template("mock_filter.html")

# Practice 题目页面（支持题目导航及收藏）
@app.route("/interview/practice_question/<int:index>", methods=["GET", "POST"])
@login_required
def practice_question(index):
    total = len(practice_questions)
    if 'practice_answers' not in session:
        session['practice_answers'] = {}
    if request.method == "POST":
        action = request.form.get("action")
        answer = request.form.get("answer")
        practice_answers = session.get('practice_answers', {})
        practice_answers[str(index)] = answer
        session['practice_answers'] = practice_answers

        if action == "next":
            return redirect(url_for("practice_question", index=index+1))
        elif action == "back":
            return redirect(url_for("practice_question", index=index-1))
        elif action == "submit":
            correct_rate = 100
            return redirect(url_for("result", mode="practice", correct_rate=correct_rate))
        elif action == "add_to_collection":
            collection_data = {
                "user_id": current_user.id,
                "question_name": f"Practice Question {index+1}",
                "industry": "Demo Industry",
                "role": "Demo Role",
                "difficulty": practice_questions[index]["difficulty"],
                "collected_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question_content": practice_questions[index]["question_content"],
                "correct_answer": "Correct answer placeholder",
                "user_answer": answer
            }
            interview_collection.insert_one(collection_data)
            flash("Question added to your collection", "success")
            return redirect(url_for("practice_question", index=index))
    
    current_answer = session.get('practice_answers', {}).get(str(index), "")
    question = practice_questions[index]
    return render_template("question.html", mode="practice", index=index, total_questions=total, question=question, current_answer=current_answer)

# Mock 题目页面（支持题目导航及收藏）
@app.route("/interview/mock_question/<int:index>", methods=["GET", "POST"])
@login_required
def mock_question(index):
    total = len(mock_questions)
    if 'mock_answers' not in session:
        session['mock_answers'] = {}
    if request.method == "POST":
        action = request.form.get("action")
        answer = request.form.get("answer")
        mock_answers = session.get('mock_answers', {})
        mock_answers[str(index)] = answer
        session['mock_answers'] = mock_answers

        if action == "next":
            return redirect(url_for("mock_question", index=index+1))
        elif action == "back":
            return redirect(url_for("mock_question", index=index-1))
        elif action == "submit":
            correct_rate = 100
            return redirect(url_for("result", mode="mock", correct_rate=correct_rate))
        elif action == "add_to_collection":
            collection_data = {
                "user_id": current_user.id,
                "question_name": f"Mock Question {index+1}",
                "industry": "Demo Industry",
                "role": "Demo Role",
                "difficulty": mock_questions[index]["difficulty"],
                "collected_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question_content": mock_questions[index]["question_content"],
                "correct_answer": "Correct answer placeholder",
                "user_answer": answer
            }
            interview_collection.insert_one(collection_data)
            flash("Question added to your collection", "success")
            return redirect(url_for("mock_question", index=index))
    
    current_answer = session.get('mock_answers', {}).get(str(index), "")
    question = mock_questions[index]
    return render_template("question.html", mode="mock", index=index, total_questions=total, question=question, current_answer=current_answer)

# 提交结果页面
@app.route("/interview/result")
@login_required
def result():
    mode = request.args.get("mode")
    correct_rate = request.args.get("correct_rate", 0)
    return render_template("result.html", correct_rate=correct_rate)

@app.route("/interview/my_collection", methods=["GET"])
@login_required
def my_collection():
    # Retrieve search parameters from the request
    question_name = request.args.get("question_name", "").strip()
    industry = request.args.get("industry", "").strip()
    role = request.args.get("role", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    collected_time = request.args.get("collected_time", "").strip()

    # Base query: Filter by user_id
    query = {"user_id": current_user.id}

    # Apply filters if user provides input
    if question_name:
        query["question_name"] = {"$regex": question_name, "$options": "i"}  # Case-insensitive
    if industry:
        query["industry"] = {"$regex": industry, "$options": "i"}
    if role:
        query["role"] = {"$regex": role, "$options": "i"}
    if difficulty:
        query["difficulty"] = difficulty  # Exact match for dropdown selection
    if collected_time:
        query["collected_time"] = {"$regex": collected_time, "$options": "i"}  # Date search

    # Query the MongoDB collection
    collections = list(interview_collection.find(query))

    return render_template("my_collection.html", collections=collections)


@app.route("/interview/my_collection/<collection_id>", methods=["GET", "POST"])
@login_required
def collection_question(collection_id):
    collection_item = interview_collection.find_one({"_id": ObjectId(collection_id)})

    if not collection_item:
        flash("Question not found", "danger")
        return redirect(url_for("my_collection"))

    if request.method == "POST":
        revised_answer = request.form.get("user_answer")
        
        interview_collection.update_one(
            {"_id": ObjectId(collection_id)},
            {"$set": {"user_answer": revised_answer}}
        )
        
        flash("Your answer has been updated!", "success")
        return redirect(url_for("collection_question", collection_id=collection_id))

    return render_template("collection_question.html",
                           difficulty=collection_item.get("difficulty"),
                           question_content=collection_item.get("question_content"),
                           correct_answer=collection_item.get("correct_answer", ""),
                           user_answer=collection_item.get("user_answer", ""))


=======
@app.route("/interview/my_collection")
@login_required
def my_collection():
    collections = list(interview_collection.find({"user_id": current_user.id}))
    return render_template("my_collection.html", collections=collections)

# 收藏题目的详情页面（只读模式，显示正确答案和用户提交答案）
@app.route("/interview/my_collection/<collection_id>")
@login_required
def collection_question(collection_id):
    collection_item = interview_collection.find_one({"_id": ObjectId(collection_id)})
    if not collection_item:
        flash("Question not found", "danger")
        return redirect(url_for("my_collection"))
    return render_template("collection_question.html", 
                           difficulty=collection_item.get("difficulty", "Unknown"),
                           question_content=collection_item.get("question_content", "????"),
                           correct_answer=collection_item.get("correct_answer", ""),
                           user_answer=collection_item.get("user_answer", ""))


# 删除收藏题目
@app.route("/interview/delete_collection/<collection_id>")
@login_required
def delete_collection(collection_id):
    interview_collection.delete_one({"_id": ObjectId(collection_id), "user_id": current_user.id})
    flash("Question deleted from your collection", "success")
    return redirect(url_for("my_collection"))



if __name__ == "__main__":
    app.run(debug=True)

