from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, mongo
from app.models import User, Post
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId

@app.route("/")
def home():
    listings = mongo.db.posts.find()
    return render_template("home.html", listings=listings)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if User.find_by_username(username):
            flash("Username already exists!", "Danger!")
        else:
            User.create(username, email, password)
            flash("Registration successful!", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.find_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!", "Danger!")
    return render_template("login.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create_lfg():
    if request.method == "POST":
        game_name = request.form["game_name"]
        level = request.form["level"]
        platform = request.form["platform"]
        description = request.form["description"]
        availability = request.form["availability"]
        region = request.form["region"]
        contact = request.form["contact"]

        Post.create(game_name, level, platform, description, availability, region, current_user.id, contact)
        flash("LFG listing created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("create_lfg.html")

@app.route("/edit/<post_id>", methods=["GET", "POST"])
@login_required
def edit_lfg(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        flash("Post not found!", "Danger!")
        return redirect(url_for("home"))

    if str(post["created_by"]) != current_user.id and not current_user.is_admin():
        flash("You do not have permission to edit this post.", "Danger!")
        return redirect(url_for("home"))

    if request.method == "POST":
        mongo.db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {
                "game_name": request.form["game_name"],
                "level": request.form["level"],
                "platform": request.form["platform"],
                "description": request.form["description"],
                "availability": request.form["availability"],
                "region": request.form["region"],
                "contact": request.form["contact"]
            }}
        )
        flash("Listing updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_lfg.html", post=post)

@app.route("/delete/<post_id>")
@login_required
def delete_lfg(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        flash("Post not found!", "Danger!")
        return redirect(url_for("home"))

    if str(post["created_by"]) != current_user.id and not current_user.is_admin():
        flash("You do not have permission to delete this post.", "Danger!")
        return redirect(url_for("home"))

    Post.delete(post_id)
    flash("Listing deleted successfully!", "success")
    return redirect(url_for("home"))
