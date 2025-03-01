from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['lost_and_found']
collection = db['items']

@app.route('/')
def home():
   
    items = list(collection.find())
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
      
        name = request.form.get('name')
        location = request.form.get('location')
        date_lost = request.form.get('date_lost')
        description = request.form.get('description')
        
        new_item = {
            'name': name,
            'location': location,
            'date_lost': date_lost,
            'description': description,
            'date_reported': datetime.now().strftime('%Y-%m-%d')
        }
        
      
        collection.insert_one(new_item)
        
      
        return redirect(url_for('home'))
    

    return render_template('add.html')


@app.route('/search')
def search_items():
    query = request.args.get('query', '')
    
    if query:
        search_query = {'name': {'$regex': query, '$options': 'i'}}
        results = list(collection.find(search_query))
    else:
        results = []
    
    return render_template('search.html', results=results)

@app.route('/details/<item_id>')
def details(item_id):
    doc = collection.find_one({'_id': ObjectId(item_id)})
    
    if not doc:
        return redirect(url_for('home'))
    
    return render_template('detail_display.html', doc=doc)

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    doc = collection.find_one({'_id': ObjectId(item_id)})
    
    if not doc:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date_lost = request.form.get('date_lost')
        description = request.form.get('description')
        
        collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {
                'name': name,
                'location': location,
                'date_lost': date_lost,
                'description': description
            }}
        )
        
        return redirect(url_for('details', item_id=item_id))

    return render_template('edit.html', doc=doc)

@app.route('/delete/<item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    doc = collection.find_one({'_id': ObjectId(item_id)})
    
    if not doc:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        collection.delete_one({'_id': ObjectId(item_id)})
        
        return redirect(url_for('home'))
    
    return render_template('delete.html', doc=doc)

if __name__ == '__main__':
    app.run(debug=True)