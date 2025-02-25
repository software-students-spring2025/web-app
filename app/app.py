from flask import Flask, render_template as rt, session, redirect, url_for, request
import pymongo
app = Flask(__name__)
app.secret_key = 'duck'

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.my_database
menu_collection = db.menu_items
menu_collection.drop()
if menu_collection.count_documents({}) == 0:
    menu_collection.insert_many([
        {'id': 'baguette', 'name': 'Baguette', 'description': 'A scrumptious baguette that would make France proud.', 'price': 1},
        {'id': 'croissant', 'name': 'Croissant', 'description': 'Decadent and Flakey. Perfect piece of bread.', 'price': 2},
        {'id': 'focaccia', 'name': 'Focaccia', 'description': 'Oven baked Italian flat bread. Very Tasty!.', 'price': 3},
        {'id': 'sourdough', 'name': 'Sourdough', 'description': "Tangy and delicious loaf that you'll love", 'price': 4},
        {'id': 'whole_grain', 'name': 'Whole Grain', 'description': "Tangy and delicious loaf that you'll love", 'price': 5},
        {'id': 'almond_cookie', 'name': 'Almond Cookie', 'description': "Delicious cookie topped with Almonds",'price': 6},
        {'id': 'chocolate_cookie', 'name': 'Chocolate Cookie', 'description': "Rich and flavorful cookie for your chocolate cravings",'price': 7},
        {'id': 'chocolate_chip_cookie', 'name': 'Chocolate Chip Cookie', 'description': "Our take on the classic simple cookie!", 'price': 8},
        {'id': 'chocolate_filled_cookie', 'name': 'Chocolate Filled Cookie', 'description': "Enjoy a crisp cookie and gooey center", 'price': 9},
        {'id': 'gingerbread', 'name': 'Gingerbread', 'description': "Enjoy the seasonal cookie all year round!", 'price': 10},
        {'id': 'matcha_cookie', 'name': 'Matcha Cookie', 'description': "Made with fresh green tea leaves at our bakery!", 'price': 11},
        {'id': 'peanut_utter_cookie', 'name': 'Peanut Butter Cookie', 'description': "Soft and chewy while being sweet and salty", 'price': 12},
        {'id': 'thumbprint_cookies', 'name': 'Thumbprint Cookies', 'description': "Shortbread Cookies with a delicious jam in the middle", 'price': 13},
    ])
menu_collection.create_index([("name", "text"), ("description", "text")])

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
    item = menu_collection.find_one({'id': item_id}, {"_id": 0})
    if not item:
        return 404
    return rt('item_info.html', item=item)

@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    cart = session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('order'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    for item_id, quantity in cart.items():
        item = menu_collection.find_one({'id': item_id}, {"_id": 0})
        if item:
            item['quantity'] = quantity
            cart_items.append(item)
    total_items = sum(cart.values())
    return rt('cart.html', cart_items=cart_items, total_items=total_items)

@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    if item_id in cart:
        if cart[item_id] > 1:
            cart[item_id] -= 1
        else:
            del cart[item_id]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    for item_id, quantity in cart.items():
        item = menu_collection.find_one({'id': item_id}, {"_id": 0})
        if item:
            item['quantity'] = quantity
            item_total = item['price'] * quantity
            item['total'] = item_total
            total_price += item_total
            cart_items.append(item)
    return rt('checkout.html', cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)