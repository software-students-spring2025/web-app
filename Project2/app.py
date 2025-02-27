#!/usr/bin/env python3

"""
LFG Web App - Flask application for gamers to find teammates.
"""

import os
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: The Flask application object
    """

    app = Flask(__name__)

    # Load Flask config from environment variables
    config = dotenv_values()
    app.config.from_mapping(config)

    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # MongoDB Connection
    try:
        cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = cxn[os.getenv("MONGO_DBNAME")]
        cxn.admin.command("ping")  # Test connection
        logging.info("✅ Connected to MongoDB successfully!")
    except Exception as e:
        logging.error("❌ MongoDB connection error:", exc_info=True)
        raise e  # Stop execution if MongoDB connection fails

    # ========================
    # 🏠 Home Route (List All Posts)
    # ========================
    @app.route("/")
    def home():
        """Displays all LFG posts sorted by creation time."""
        try:
            posts = list(db.posts.find({}).sort("created_at", -1))
            return render_template("index.html", posts=posts)
        except Exception as e:
            logging.error(f"⚠️ Error fetching posts: {e}", exc_info=True)
            return render_template("error.html", error="Could not load posts."), 500

    # ========================
    # 📝 Create a New Post
    # ========================
    @app.route("/create", methods=["POST"])
    def create_post():
        """Creates a new LFG post and saves it to the database."""
        try:
            # Required fields
            required_fields = ["game_name", "level", "platform", "role", "description", "availability", "region", "created_by", "contact"]

            # Validate input
            if not all(field in request.form and request.form[field] for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            # Store data safely
            new_post = {
                **{key: request.form[key] for key in required_fields},
                "created_at": datetime.datetime.utcnow(),
            }

            db.posts.insert_one(new_post)
            return redirect(url_for("home"))
        except Exception as e:
            logging.error(f"⚠️ Error creating post: {e}", exc_info=True)
            return render_template("error.html", error="Could not create post."), 500

    # ========================
    # ✏️ Edit an Existing Post
    # ========================
    @app.route("/edit/<post_id>")
    def edit(post_id):
        """Displays a form to edit an existing LFG post."""
        try:
            post = db.posts.find_one({"_id": ObjectId(post_id)})
            if not post:
                return render_template("error.html", error="Post not found."), 404
            return render_template("edit.html", post=post)
        except Exception as e:
            logging.error(f"⚠️ Error fetching post for editing: {e}", exc_info=True)
            return render_template("error.html", error="Could not load post."), 500

    @app.route("/edit/<post_id>", methods=["POST"])
    def edit_post(post_id):
        """Updates an existing post in the database."""
        try:
            update_data = {
                **{key: request.form[key] for key in ["game_name", "level", "platform", "role", "description", "availability", "region", "contact"]},
                "updated_at": datetime.datetime.utcnow(),
            }

            result = db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})
            if result.matched_count == 0:
                return render_template("error.html", error="Post not found."), 404

            return redirect(url_for("home"))
        except Exception as e:
            logging.error(f"⚠️ Error updating post: {e}", exc_info=True)
            return render_template("error.html", error="Could not update post."), 500

    # ========================
    # 🗑 Delete a Post
    # ========================
    @app.route("/delete/<post_id>", methods=["POST"])
    def delete(post_id):
        """Deletes an LFG post from the database."""
        try:
            result = db.posts.delete_one({"_id": ObjectId(post_id)})
            if result.deleted_count == 0:
                return jsonify({"error": "Post not found"}), 404
            return jsonify({"message": "Post deleted successfully"}), 200
        except Exception as e:
            logging.error(f"⚠️ Error deleting post: {e}", exc_info=True)
            return jsonify({"error": "Could not delete post"}), 500

    # ========================
    # 🔎 Search Posts by Filters
    # ========================
    @app.route("/search", methods=["GET"])
    def search():
        """Searches for LFG posts based on game name and level."""
        try:
            game = request.args.get("game")
            level = request.args.get("level")
            query = {}

            if game:
                query["game_name"] = {"$regex": game, "$options": "i"}  # Case-insensitive search
            if level:
                query["level"] = level

            results = list(db.posts.find(query).sort("created_at", -1))
            return render_template("search_results.html", posts=results)
        except Exception as e:
            logging.error(f"⚠️ Error searching posts: {e}", exc_info=True)
            return render_template("error.html", error="Search failed."), 500

    # ========================
    # 🔐 Admin: Delete Inappropriate Posts
    # ========================
    @app.route("/admin/delete/<post_id>", methods=["DELETE"])
    def admin_delete_post(post_id):
        """Admin can delete inappropriate posts."""
        try:
            db.posts.delete_one({"_id": ObjectId(post_id)})
            return jsonify({"message": "Post removed by admin."}), 200
        except Exception as e:
            logging.error(f"⚠️ Admin delete error: {e}", exc_info=True)
            return jsonify({"error": "Could not delete post"}), 500

    # ========================
    # ⚠️ Error Handling
    # ========================
    @app.errorhandler(Exception)
    def handle_error(e):
        """Global error handler."""
        logging.error(f"⚠️ Unhandled error: {e}", exc_info=True)
        return render_template("error.html", error=str(e)), 500

    return app

app = create_app()

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    print(f"✅ Flask running on port {FLASK_PORT}")
    app.run(port=int(FLASK_PORT), debug=True)
