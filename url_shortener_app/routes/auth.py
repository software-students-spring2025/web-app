from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = User.find_by_username(username)
        if user_data and User(user_data["_id"], user_data["username"], user_data["password_hash"]).verify_password(password):
            user = User(user_data["_id"], user_data["username"], user_data["password_hash"])
            login_user(user)
            return redirect(url_for("urls.dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.create_user(username, password)
        if user:
            return redirect(url_for("auth.login"))
        flash("Username already exists")
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
