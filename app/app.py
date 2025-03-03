from flask import Flask, render_template as rt, session, redirect, url_for, request
from flask_pymongo import PyMongo
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'duck'
import os, uuid
from dotenv import load_dotenv
load_dotenv()

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/anatidelicious") 
# if this error: AttributeError: 'NoneType' object has no attribute 'menu_items'
# run $export MONGO_URI= "mongodb://localhost:27017/anatidelicious" in terminal

mongo = PyMongo(app)
db = mongo.db

app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_MONGO"] = mongo.cx
Session(app)

menu_collection = db.menu_items
menu_collection.drop() # if we drop this, the cart resets every time, cart information not saved for customer
carts = db.carts
#carts.drop()
orders = db.orders

if menu_collection.count_documents({}) == 0:
    menu_collection.insert_many([
        {'item_id': 'baguette', 'name': 'Baguette', 'description': 'A scrumptious baguette that would make France proud.', 'price': 1, 'category': 'Breads', 'allergy_info': 'gluten, dairy, eggs', 'calories': 185},
        {'item_id': 'croissant', 'name': 'Croissant', 'description': 'Decadent and Flakey. Perfect piece of bread.', 'price': 2, 'category': 'Breads', 'allergy_info': 'gluten, dairy, eggs', 'calories': 230},
        {'item_id': 'focaccia', 'name': 'Focaccia', 'description': 'Oven baked Italian flat bread. Very Tasty!.', 'price': 3, 'category': 'Breads', 'allergy_info': 'gluten, dairy, eggs', 'calories': 140},
        {'item_id': 'sourdough', 'name': 'Sourdough', 'description': "Tangy and delicious loaf that you'll love",  'price': 4, 'category': 'Breads', 'allergy_info': 'gluten, dairy, eggs', 'calories': 185},
        {'item_id': 'whole_grain', 'name': 'Whole Grain', 'description': "Nutritious bread full of whole grains",  'price': 5, 'category': 'Breads', 'allergy_info': 'gluten, dairy, eggs', 'calories': 70},
        {'item_id': 'almond_cookie', 'name': 'Almond Cookie', 'description': "Delicious cookie topped with Almonds", 'price': 6, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs, tree nuts', 'calories': 50},
        {'item_id': 'chocolate_cookie', 'name': 'Chocolate Cookie', 'description': "Rich and flavorful cookie for your chocolate cravings", 'price': 7, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 200},
        {'item_id': 'chocolate_chip_cookie', 'name': 'Chocolate Chip Cookie', 'description': "Our take on the classic simple cookie!", 'price': 8, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 80},
        {'item_id': 'chocolate_filled_cookie', 'name': 'Chocolate Filled Cookie', 'description': "Enjoy a crisp cookie and gooey center", 'price': 9, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 185},
        {'item_id': 'gingerbread', 'name': 'Gingerbread', 'description': "Enjoy the seasonal cookie all year round!", 'price': 10, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 220},
        {'item_id': 'matcha_cookie', 'name': 'Matcha Cookie', 'description': "Made with fresh green tea leaves at our bakery!", 'price': 11, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 150},
        {'item_id': 'peanut_butter_cookie', 'name': 'Peanut Butter Cookie', 'description': "Soft and chewy while being sweet and salty", 'price': 12, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs, peanuts', 'calories': 135},
        {'item_id': 'thumbprint_cookies', 'name': 'Thumbprint Cookies', 'description': "Shortbread Cookies with a delicious jam in the middle", 'price': 13, 'category': 'Cookies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 140},
        {'item_id': 'carrot_cake', 'name': 'Carrot Cake', 'description': "A sweet carrot cake with a cream cheese icing", 'price': 14, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 185},
        {'item_id': 'cheese_cake', 'name': 'Cheese Cake',  'description': "Made with fresh cream cheese and a cookie base", 'price': 15, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 400},
        {'item_id': 'chocolate_berry_cake', 'name': 'Chocolate Berry Cake', 'description': "Moist Chocolate cake topped with Mixed Berries!", 'price': 16, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 350},
        {'item_id': 'chocolate_mousse_cake', 'name': 'Chocolate Mousse Cake',  'description': "Enjoy a cake with fluffy chocolate mousse", 'price': 17, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 500},
        {'item_id': 'rainbow_cake', 'name': 'Rainbow Cake', 'description': "Seven layer cake of colorful and delicious ingredients!", 'price': 18, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 250},
        {'item_id': 'red_velvet', 'name': 'Red Velvet',  'description': "Cake with a rich red color and cream cheese frosting", 'price': 19, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 600},
        {'item_id': 'strawberry_shortcake', 'name': 'Strawberry Shortcake',  'description': "Crisp, crumbly cake with whipped frosting and fresh strawberries", 'price': 20, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 300},
        {'item_id': 'white_cake', 'name': 'White Cake', 'description': "Vanilla cake with frosting, cream, and seasonal berries", 'price': 21, 'category': 'Cakes', 'allergy_info': 'gluten, dairy, eggs', 'calories': 250},
        {'item_id': 'almond_donut', 'name': 'Almond Donut', 'description': "Plain donut with chocolate frosting and almonds", 'price': 22, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs, tree nuts', 'calories': 190},
        {'item_id': 'caramel_donut', 'name': 'Caramel Donut', 'description': "Topped with a caramel glaze and a caramel drizzle", 'price': 23, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 250},
        {'item_id': 'chocolate_glazed', 'name': 'Chocolate Glazed Donut', 'description': "Beautiful rich chocolate glaze with a chocolate drizzle", 'price': 24, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 300},
        {'item_id': 'cookies_and_cream', 'name': 'Cookies and Cream Donut',  'description': "Chocolate donut with frosting and cookie crumble", 'price': 25, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 300},
        {'item_id': 'glazed_donut', 'name': 'Glazed Donut', 'description': "The classic delicious glazed donut! Perfect for breakfast", 'price': 26, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 180},
        {'item_id': 'pink_sprinkled', 'name': 'Pink Sprinkled Donut', 'description': "Plain donut topped entirely in pink sprinkles", 'price': 27, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 200},
        {'item_id': 'jam_and_sugar', 'name': 'Jam and Sugar Donut',  'description': "Plain donut topped with strawberry jam and sugar", 'price': 28, 'category': 'Donuts', 'allergy_info': 'gluten, dairy, eggs', 'calories': 190},
        {'item_id': 'apple_pie', 'name': 'Apple Pie', 'description': "Classic apple pie topped with sugar", 'price': 29, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 270},
        {'item_id': 'apricot_pie', 'name': 'Apricot Pie', 'description': "Made with fresh Apricots and nutmeg", 'price': 30, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 250},
        {'item_id': 'custard_pie', 'name': 'Custard Pie', 'description': "Silky and Sweet Custard pie with a crumb coat", 'price': 31, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 220},
        {'item_id': 'key_lime_pie', 'name': 'Key Lime Pie', 'description': "A bright tangy yet sweet pie", 'price': 32, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 380},
        {'item_id': 'pecan_pie', 'name': 'Pecan Pie', 'description': "A pie made of pecan nuts and uses cane syrup", 'price': 33, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs, tree nuts', 'calories': 500},
        {'item_id': 'pumpkin_pie', 'name': 'Pumpkin Pie', 'description': "The perfect fall pie! Made with nutmeg and ginger!", 'price': 34, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 320},
        {'item_id': 'cherry_pie', 'name': 'Cherry Pie',  'description': "Beautiful pie made with fresh delicious cherries", 'price': 35, 'category': 'Pies', 'allergy_info': 'gluten, dairy, eggs', 'calories': 480},
        {'item_id': 'avocado_toast', 'name': 'Avocado Toast', 'description': "Toast topped with mashed avocado and an egg", 'price': 36, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs', 'calories': 300},
        {'item_id': 'blt', 'name': 'BLT', 'description': "Bacon, lettuce, mayo, and tomato on yummy white bread",  'price': 37, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs', 'calories': 300},
        {'item_id': 'breakfast_sandwich', 'name': 'Breakfast Sandwich',  'description': "Sausage, egg, cheese, and bacon on an english muffin!", 'price': 38, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs', 'calories': 400},
        {'item_id': 'grilled_cheese', 'name': 'Grilled Cheese',  'description': "Classic cheese sandwich made with american cheese", 'price': 39, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs', 'calories': 400},
        {'item_id': 'pb_and_j', 'name': 'PB and J', 'description': "Delicious combo of Peanut butter and Jelly on multigrain bread!", 'price': 40, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs, peanuts', 'calories': 350},
        {'item_id': 'salmon_sandwich', 'name': 'Salmon Sandwich', 'description': "Beautiful salmon paired with fresh veggies", 'price': 41, 'category': 'Sandwiches', 'allergy_info': 'gluten, dairy, eggs', 'calories': 500},
    ])

menu_collection.create_index([("name", "text"), ("description", "text")])

from models.Cart import Cart
# from models.MenuItem import MenuItem
from models.Order import Order

@app.route("/")
def home():
    return rt('home.html')

@app.route('/login')
def login():
    return rt('login.html')

@app.route('/contact')
def contact():
    return rt('contact.html')

'''
TODO: Change categories so that you can search on the home page and get all results
that match a certain keyword regardless of category
'''
@app.route('/order', methods=['GET'])
def order():
    category = request.args.get('category', '').strip()
    query = request.args.get('query', '').strip()
    filter_query = {}
    if category:
        filter_query['category'] = category
    if query:
        regex = {"$regex": query, "$options": "i"}
        filter_query["$or"] = [{"name": regex}, {"description": regex}]
    menu_items = list(menu_collection.find(filter_query, {"_id": 0})) if category or query else []
    categories = menu_collection.distinct('category')
    return rt('order.html', menu_items=menu_items, category=category, categories=categories, query=query)

@app.route('/item_info/<item_id>')
def item_info(item_id):
    item = menu_collection.find_one({'item_id': item_id})
    if not item:
        return 404
    return rt('item_info.html', item=item)

@app.before_request
def initialize_cart():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    customer_id = session.get('user_id')
    category = request.args.get('category')
    query = request.args.get('query', '')
    if not customer_id:
        return redirect(url_for('login'))
    Cart.add_to_cart(customer_id, item_id)

    referer = request.referrer or url_for('order')
    return redirect(referer)


@app.route('/cart')
def cart():
    customer_id = session.get('user_id')

    if not customer_id:
        return redirect(url_for('login'))

    cart = Cart.get_cart(customer_id)

    cart_items = []
    total_price = cart.get('total_price', 0)
    total_items = 0

    for item_id in sorted(list(set(cart.get('items')))):
        item = menu_collection.find_one({'item_id': item_id})
        if item:
            item_quantity = Cart.get_item_count(customer_id, item_id)
            if item_quantity > 0:
                total_items += item_quantity
                item['quantity'] = item_quantity
                item['total'] = Cart.get_item_count(customer_id, item_id) * item.get('price')
                cart_items.append(item)
    print(cart_items)
    return rt('cart.html', cart_items=cart_items, total_items=total_items)


@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):
    customer_id = session.get('user_id')

    if not customer_id:
        return redirect(url_for('login'))
    
    cart = Cart.get_cart(customer_id)
    
    Cart.remove_from_cart(customer_id, item_id)

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['GET', 'POST'])
def clear_cart():
    customer_id = session.get('user_id')
    Cart.clear_cart(customer_id)

    referer = request.referrer or url_for('cart')
    return redirect(referer)

@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    customer_id = session.get('user_id')

    if not customer_id:
        return redirect(url_for('login'))

    cart = Cart.get_cart(customer_id)
    cart_items = []
    total_price = Cart.calculate_raw_total(customer_id)
    for item_id in sorted(list(set(cart.get('items')))):
        item = menu_collection.find_one({'item_id': item_id})
        if item and Cart.get_item_count(customer_id, item_id) > 0:
            item['quantity'] = Cart.get_item_count(customer_id, item_id)
            item['total'] = Cart.get_item_count(customer_id, item_id) * item.get('price')
            cart_items.append(item)
    return rt('checkout.html', cart_items=cart_items, total_price=total_price)


@app.route('/submit_order', methods=['POST'])
def submit_order():
    customer_id = session.get('user_id')

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    delivery_method = request.form.get('delivery_method')
    shipping_address = request.form.get('shipping_address') if delivery_method == "delivery" else None
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    zip_code = request.form.get('zip')

    if not card_number.isdigit() or len(card_number) != 16:
        return "Invalid card number. Card number must be 16 digits.", 400

    if not cvv.isdigit() or len(cvv) != 3:
        return "Invalid card number. CVV must be 3 digits.", 400

    if not zip_code.isdigit() or len(zip_code) != 5:
        return "Invalid zip code. Zip code must be 5 digits.", 400
    
    print("Is method delivery: ", delivery_method, (delivery_method == 'delivery'))
    print("Shipping address: ", shipping_address)
    
    if delivery_method == "delivery" and not shipping_address:
        return "Please enter shipping address for delivery", 400

    if shipping_address:
        Order.submit_order(customer_id, first_name, last_name, email, card_number, cvv, zip_code, delivery_method, shipping_address)
    else:
        Order.submit_order(customer_id, first_name, last_name, email, card_number, cvv, zip_code, delivery_method)
    
    
    return redirect(url_for('view_orders'))

@app.route('/view_orders', methods=['GET', 'POST'])
def view_orders():
    customer_id = session.get('user_id')
    orders = Order.view_orders(customer_id)

    return rt('view_orders.html', orders=orders)


@app.route('/delete_order/<order_id>')
def delete_order(order_id):
    customer_id = session.get('user_id')

    Order.delete_order(order_id, customer_id)

    return redirect(url_for('view_orders'))

if __name__ == "__main__":
    app.run(debug=True)