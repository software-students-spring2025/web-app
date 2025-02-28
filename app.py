from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db = client.get_default_database()
collection = db.sales

# Home Page - View all products
@app.route('/')
def home():
    products = list(collection.find())
    return render_template('home.html', products=products)

# Add New Product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        item = request.form['item']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        # Insert into MongoDB
        collection.insert_one({
            'item': item,
            'price': price,
            'quantity': quantity
        })
        flash('Product added successfully!')
        return redirect(url_for('home'))
    return render_template('add.html')

# Edit Product
@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = collection.find_one({'_id': product_id})
    if request.method == 'POST':
        item = request.form['item']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        # Update MongoDB
        collection.update_one({'_id': product_id}, {'$set': {
            'item': item,
            'price': price,
            'quantity': quantity
        }})
        flash('Product updated successfully!')
        return redirect(url_for('home'))
    return render_template('edit.html', product=product)

# Delete Product
@app.route('/delete/<product_id>')
def delete_product(product_id):
    collection.delete_one({'_id': product_id})
    flash('Product deleted successfully!')
    return redirect(url_for('home'))

# Search Product
@app.route('/search', methods=['GET', 'POST'])
def search_product():
    if request.method == 'POST':
        query = request.form['query']
        products = list(collection.find({'item': {'$regex': query, '$options': 'i'}}))
        return render_template('home.html', products=products)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)
