from flask import Flask, jsonify, request, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv, dotenv_values
from bson.objectid import ObjectId

# Load environment variables

load_dotenv()

def create_app():
    """
    Create and configure the Flask application.
    Returns: app: the Flask application object
    """
    app = Flask(__name__)

    # Load Flask config from .env variables
    config = dotenv_values()
    app.config.from_mapping(config)

    # Connect to MongoDB
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DBNAME")]
    # books_collection = db["books"]

    # Testing 
    print("Collections:", db.list_collection_names())
    print("Books:", list(db["books"].find({}).limit(5)))

    try:
        client.admin.command("ping")
        print("* Connected to MongoDB!")
    except Exception as e:
        print("* MongoDB connection error:", e)

    # Routes

    @app.route("/")
    def home():
        """
        Route for the home page.
        Returns: Rendered template (str): The rendered HTML template.
        """
        books = list(db["books"].find({}))  
        return render_template("index.html", books=books)

    @app.route("/add-book", methods=["GET", "POST"])
    def add_book():
        """
        Renders the add book form page and handles new book submissions.
        """
        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")
            edition = request.form.get("edition")
            year = request.form.get("year")
            condition = request.form.get("condition")
            price = request.form.get("price")
            book_format = request.form.get("format")
            
           
            if not title or not author or not year or not price:
                return jsonify({"error": "Missing required fields"}), 400

            new_book = {
                "title": title,
                "author": author,
                "edition": edition,
                "year": int(year),
                "condition": condition,
                "price": float(price),
                "format": book_format,
            }
            
            db.books.insert_one(new_book)

            return redirect(url_for("home"))
        return render_template("add_book.html")

    @app.route("/book/<book_id>")
    def book_details(book_id):
        """
        Route to display the details of a selected book.
        """
        book = db.books.find_one({"_id": ObjectId(book_id)})
        
        if not book:
            return "Book not found", 404

        return render_template("book_details.html", book=book)

    return app

# Run the Flask app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

