import flask
import src.db as db
import config

app = flask.Flask(__name__)
app.secret_key = "super secret key"
cur_user = None

db.init_db(app)

# Index get
@app.route('/')
def index():
    return flask.redirect('/home')

# Login get
@app.route('/login')
def login():
    flask.session.clear() # Clear the session and force user to login
    return flask.render_template('login.html')

# Login post if user give username and password
@app.route('/login', methods=['POST'])
def handle_login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    
    user = db.login_user(username, password)
    # Redirect if find match user in the database
    if user:  
        flask.session['user'] = user.get('username')
        print("Current User: " + flask.session['user'])
        return flask.redirect('/home')

    return flask.render_template('login.html', message="Invalid username or password")

# Register get
@app.route('/register')
def register():
    return flask.render_template('register.html')

# Register the username and possword
@app.route('/register', methods=['POST'])
def handle_register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    db.create_user(username, password)
    user = db.login_user(username, password)

    if user:
        flask.session['user'] = user.get('username')
        print("Current User: " + flask.session['user'])
        return flask.redirect('/home')

    return flask.render_template('register.html', message="Username Already Exist or Passwork too Short")

# Logout (no actual page)
@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect('/login')

# Homepage get
@app.route('/home')
def home():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    user = flask.session['user']
    print("Current User: " + user)
    search_keyword = flask.request.args.get('search', '').strip()
    if search_keyword:
        orders = db.search_orders(user, search_keyword)
    else:
        orders = db.find_user_order(user)
    # print(orders)
    orderNum = len(orders)
    # print("Total Num"+ str(orderNum))
    return flask.render_template('home.html', orders=orders, length =orderNum, user=user)

# DetailPage get Without Order ID
@app.route('/detail')
def detail_no_id():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return flask.redirect('/home')

# DetailPage get with Order ID
@app.route('/detail/<order_id>')
def detail(order_id): 
    if 'user' not in flask.session:
        return flask.redirect('/login')
    order = db.get_order(order_id)
    return flask.render_template('detail.html', order=order)

# DetailPage Post
@app.route('/detail/<order_id>', methods=['POST'])
def handle_detail(order_id):
    order = db.get_order(order_id)
    updated_data = {
        "consumer": flask.request.form.get("customerName"),
        "food": flask.request.form.get("dishName"),
        "address": flask.request.form.get("address"),
        "price": float(flask.request.form.get("price")),  
        "contact": flask.request.form.get("contact")
    }
    result = db.update_order(order_id, updated_data)
    if result: 
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('detail.html', order=order)

# Delete Order in DetailPage
@app.route('/detail/<order_id>/delete') # Don't delete "/delete" 
def delete_order(order_id):
    if 'user' not in flask.session:
        return flask.redirect('/login')
    db.delete_order(order_id)
    return flask.redirect('/home')

# NewOrder get
@app.route('/newOrder')
def order():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    user = flask.session['user']
    return flask.render_template('add.html', user=user)

# NewOrder Post
@app.route('/newOrder', methods=['POST'])
def handle_order(): 
    if 'user' not in flask.session:
        return flask.redirect('/login')
    user_name = flask.request.form.get('user_name')
    name = flask.request.form.get('name')
    food = flask.request.form.get('food')
    address = flask.request.form.get('address')
    price = flask.request.form.get('price')
    db.create_order(user_name, name, food, address, price, contact)
    return flask.redirect('/home')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000) # run this line can see it on phone or computer
    # app.run(debug=True, port=config.PORT, ) # run this line can see it on computer

