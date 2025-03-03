#!/usr/bin/env python3

"""
NYU Lost and Found Flask Application
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

# load environment variables from .env file
load_dotenv()

def create_app():
    """
    Create and configure the Flask application
    Returns: Flask application object
    """
    app = Flask(__name__, template_folder='templates', static_folder='templates')
    
    # Connect to MongoDB
    # Use environment variable MONGO_URI if set, otherwise use default
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    mongo_dbname = os.getenv("MONGO_DBNAME", "lost_and_found")
    
    try:
        client = pymongo.MongoClient(mongo_uri)
        # Test connection
        client.admin.command("ping")
        print(" * Successfully connected to MongoDB!")
        db = client[mongo_dbname]
        collection = db['items']
    except Exception as e:
        print(" * MongoDB connection error:", e)
        # Continue with app setup even if MongoDB connection fails
        # This allows the app to start and show appropriate errors
        db = None
        collection = None
    
    # Home route
    @app.route('/')
    def home():
        """
        Route for the home page
        Returns: rendered template
        """
        if collection is not None:
            items = list(collection.find())
        else:
            items = []
            # If MongoDB is unavailable, you might want to show an error
            app.logger.error("MongoDB is unavailable")
        
        return render_template('index.html', items=items)
    
    # Add new item page
    @app.route('/add', methods=['GET', 'POST'])
    def add_item():
        """
        Route for adding items
        Handles GET requests to display form and POST requests to add new items
        """
        if request.method == 'POST':
            if collection is None:
                # Return a simple error message since error.html is not ready
                return "Database connection is unavailable. Please try again later.", 503
                
            # Get form data
            name = request.form.get('name')
            location = request.form.get('location')
            date_lost = request.form.get('date_lost')
            description = request.form.get('description')
            
            # Create new document
            new_item = {
                'name': name,
                'location': location,
                'date_lost': date_lost,
                'description': description,
                'date_reported': datetime.datetime.utcnow()
            }
            
            # Insert into database
            collection.insert_one(new_item)
            
            # Redirect to home page
            return redirect(url_for('home'))
        
        # Display add page for GET requests
        return render_template('add.html')
    
    # Search page
    @app.route('/search')
    def search_items():
        """
        Route for searching items
        """
        query = request.args.get('query', '')
        
        if collection is None:
            # Return a simple error message since error.html is not ready
            return "Database connection is unavailable. Please try again later.", 503
            
        # Execute search if query exists
        if query:
            # Use regex for case-insensitive search
            search_query = {'name': {'$regex': query, '$options': 'i'}}
            results = list(collection.find(search_query))
        else:
            results = []
        
        return render_template('search.html', results=results)
    
    # Item details page
    @app.route('/details/<item_id>')
    def details(item_id):
        """
        Route for item details
        Parameters:
            item_id (str): The ID of the item
        """
        if collection is None:
            # Return a simple error message since error.html is not ready
            return "Database connection is unavailable. Please try again later.", 503
            
        # Get item by ID
        doc = collection.find_one({'_id': ObjectId(item_id)})
        
        # Redirect to home if item not found
        if not doc:
            return redirect(url_for('home'))
        
        return render_template('detail_display.html', doc=doc)
    
    # Edit item
    @app.route('/edit/<item_id>', methods=['GET', 'POST'])
    def edit_item(item_id):
        """
        Route for editing items
        Parameters:
            item_id (str): The ID of the item
        """
        if collection is None:
            # Return a simple error message since error.html is not ready
            return "Database connection is unavailable. Please try again later.", 503
            
        # Get item
        doc = collection.find_one({'_id': ObjectId(item_id)})
        
        # Redirect to home if item not found
        if not doc:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            location = request.form.get('location')
            date_lost = request.form.get('date_lost')
            description = request.form.get('description')
            
            # Update document
            collection.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': {
                    'name': name,
                    'location': location,
                    'date_lost': date_lost,
                    'description': description,
                    'last_updated': datetime.datetime.utcnow()
                }}
            )
            
            # Redirect to details page
            return redirect(url_for('details', item_id=item_id))
        
        # Display edit page for GET requests
        return render_template('edit.html', doc=doc)
    
    # Delete item
    @app.route('/delete/<item_id>', methods=['GET', 'POST'])
    def delete_item(item_id):
        """
        Route for deleting items
        Parameters:
            item_id (str): The ID of the item
        """
        if collection is None:
            # Return a simple error message since error.html is not ready
            return "Database connection is unavailable. Please try again later.", 503
            
        # Get item
        doc = collection.find_one({'_id': ObjectId(item_id)})
        
        # Redirect to home if item not found
        if not doc:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            # Delete from database
            collection.delete_one({'_id': ObjectId(item_id)})
            
            # Redirect to home page
            return redirect(url_for('home'))
        
        # Display confirmation page for GET requests
        return render_template('delete.html', doc=doc)
    
    # Error handling - Using the error.html template
    @app.errorhandler(Exception)
    def handle_error(e):
        """
        Handle any errors
        Parameters:
            e (Exception): The exception object
        """
        app.logger.error(f"An error occurred: {e}")
        
        # Get error code or default to 500
        error_code = getattr(e, 'code', 500)
        
        # Return rendered error template with appropriate error details
        return render_template('error.html', 
                            error_code=error_code,
                            error_message=str(e)), error_code
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment variables (default to 5001)
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")
    
    # Run the application with host='0.0.0.0' to make it accessible from outside the container
    app.run(host='0.0.0.0', debug=(FLASK_ENV == "development"), port=int(FLASK_PORT))