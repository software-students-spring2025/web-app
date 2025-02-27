from flask import Flask, render_template as rt, session, redirect, url_for, request
from flask_pymongo import PyMongo
app = Flask(__name__)
app.secret_key = 'duck'
import os
from dotenv import load_dotenv
load_dotenv()

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/anatidelicious") 
# if this error: AttributeError: 'NoneType' object has no attribute 'menu_items'
# run $export MONGO_URI= "mongodb://localhost:27017/anatidelicious" in terminal

mongo = PyMongo(app)
db = mongo.db  

menu_collection = db.menu_items
menu_collection.drop() # if we drop this, the cart resets every time, cart information not saved for customer
carts = db.carts
carts.drop()
if menu_collection.count_documents({}) == 0:
    menu_collection.insert_many([
        {'item_id': 'baguette', 'name': 'Baguette', 'description': 'A scrumptious baguette that would make France proud.', 'price': 1},
        {'item_id': 'croissant', 'name': 'Croissant', 'description': 'Decadent and Flakey. Perfect piece of bread.', 'price': 2},
        {'item_id': 'focaccia', 'name': 'Focaccia', 'description': 'Oven baked Italian flat bread. Very Tasty!.', 'price': 3},
        {'item_id': 'sourdough', 'name': 'Sourdough', 'description': "Tangy and delicious loaf that you'll love", 'price': 4},
        {'item_id': 'whole_grain', 'name': 'Whole Grain', 'description': "Tangy and delicious loaf that you'll love", 'price': 5},
        {'item_id': 'almond_cookie', 'name': 'Almond Cookie', 'description': "Delicious cookie topped with Almonds",'price': 6},
        {'item_id': 'chocolate_cookie', 'name': 'Chocolate Cookie', 'description': "Rich and flavorful cookie for your chocolate cravings",'price': 7},
        {'item_id': 'chocolate_chip_cookie', 'name': 'Chocolate Chip Cookie', 'description': "Our take on the classic simple cookie!", 'price': 8},
        {'item_id': 'chocolate_filled_cookie', 'name': 'Chocolate Filled Cookie', 'description': "Enjoy a crisp cookie and gooey center", 'price': 9},
        {'item_id': 'gingerbread', 'name': 'Gingerbread', 'description': "Enjoy the seasonal cookie all year round!", 'price': 10},
        {'item_id': 'matcha_cookie', 'name': 'Matcha Cookie', 'description': "Made with fresh green tea leaves at our bakery!", 'price': 11},
        {'item_id': 'peanut_utter_cookie', 'name': 'Peanut Butter Cookie', 'description': "Soft and chewy while being sweet and salty", 'price': 12},
        {'item_id': 'thumbprint_cookies', 'name': 'Thumbprint Cookies', 'description': "Shortbread Cookies with a delicious jam in the middle", 'price': 13},
    ])

menu_collection.create_index([("name", "text"), ("description", "text")])

from models.Cart import Cart
from models.MenuItem import MenuItem

@app.route("/")
def home():
    return rt('home.html')

@app.route('/login')
def login():
    return rt('login.html')

@app.route('/contact')
def contact():
    return rt('contact.html')

@app.route('/order')
def order():
    query = request.args.get('query', '').strip()
    if query:
        regex = {"$regex": query, "$options": "i"}
        menu_items = list(menu_collection.find(
            {"$or": [{"name": regex}, {"description": regex}]},
            {"_id": 0}))
    else:
        menu_items = list(menu_collection.find({}, {"_id": 0}))
    return rt('order.html', menu_items=menu_items)

@app.route('/item_info/<item_id>')
def item_info(item_id):
    item = menu_collection.find_one({'item_id': item_id})
    if not item:
        return 404
    return rt('item_info.html', item=item)

@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    customer_id = 100 # placeholder value

    if not customer_id:
        return redirect(url_for('login'))
    Cart.add_to_cart(customer_id, item_id)

    return redirect(url_for('order'))


@app.route('/cart')
def cart():
    customer_id = 100 # placeholder value

    if not customer_id:
        return redirect(url_for('login'))

    cart = Cart.get_cart(customer_id)

    cart_items = []
    total_price = cart.get('total_price', 0)
    total_items = 0

    for item_id in set(cart.get('items')):
        item = menu_collection.find_one({'item_id': item_id})
        if item:
            item_quantity = Cart.get_item_count(customer_id, item_id)
            if item_quantity > 0:
                total_items += item_quantity
                item['quantity'] = item_quantity
                cart_items.append(item)
    print(cart_items)
    return rt('cart.html', cart_items=cart_items, total_items=total_items)


@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):
    customer_id = 100 # placeholder value

    if not customer_id:
        return redirect(url_for('login'))
    
    cart = Cart.get_cart(customer_id)
    
    Cart.remove_from_cart(customer_id, item_id)

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    customer_id = 100 # placeholder value

    if not customer_id:
        return redirect(url_for('login'))

    cart = Cart.get_cart(customer_id)
    cart_items = []
    total_price = Cart.calculate_raw_total(customer_id)
    for item_id in set(cart.get('items')):
        item = menu_collection.find_one({'item_id': item_id})
        if item and Cart.get_item_count(customer_id, item_id) > 0:
            item['quantity'] = Cart.get_item_count(customer_id, item_id)
            item['total'] = Cart.get_item_count(customer_id, item_id) * item.get('price')
            cart_items.append(item)
    return rt('checkout.html', cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)