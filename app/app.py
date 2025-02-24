from flask import Flask, render_template as rt, session, redirect, url_for, request
app = Flask(__name__)
app.secret_key = 'duck'

#This is just a temp database which I will later replace with a mongoDB database
menu_items = [
    {'id': 'scone', 'name': 'Scone', 'description': 'Tasty savory scone made with love.', 'price': 5},
    {'id': 'croissant', 'name': 'Croissant', 'description': 'Made fresh this morning by real ducks.', 'price': 3},
    {'id': 'salad', 'name': 'Salad', 'description': 'Contains high fructose corn syrup.', 'price': 1000}
    ]

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
    query = request.args.get('query', '').strip().lower()
    if query:
        filtered = [item for item in menu_items if query in item['name'].lower() or query in item['description'].lower()]
    else:
        filtered = menu_items
    return rt('order.html', menu_items=filtered)

@app.route('/item_info/<item_id>')
def item_info(item_id):
    item = next((item for item in menu_items if item['id'] == item_id), None)
    if not item:
        return f"Item '{item_id}' not found.", 404
    return rt('item_info.html', item=item)

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
    for item in menu_items:
        if item['id'] in cart:
            item_copy = item.copy()
            item_copy['quantity'] = cart[item['id']]
            cart_items.append(item_copy)
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
    for item in menu_items:
        if item['id'] in cart:
            item_copy = item.copy()
            item_copy['quantity'] = cart[item['id']]
            item_total = item_copy['price'] * item_copy['quantity']
            item_copy['total'] = item_total
            total_price += item_total
            cart_items.append(item_copy)
    return rt('checkout.html', cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)