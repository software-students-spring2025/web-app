from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_session import Session  # Flask session management
import os
from bson import ObjectId  # Fixes ObjectId issue for MongoDB
from werkzeug.utils import secure_filename

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Secret key for session security (Ensure it's properly loaded from .env)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Flask session config (for session persistence)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# MongoDB Configuration
atlas_uri = os.getenv('MONGO_URI')  # Check if MONGO_URI is set in .env
if atlas_uri:
    # If MONGO_ATLAS_URI is set, use it
    app.config['MONGO_URI'] = atlas_uri
    print("Using Atlas URI:", atlas_uri)
else:
    app.config['MONGO_URI'] = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORT', '27017')}/{os.getenv('MONGO_DB', 'project2')}"

# Initialize PyMongo
mongo = PyMongo(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Picture Upload Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# User Model
class User(UserMixin):
    def __init__(self, username, email, password_hash, _id=None):
        self.id = str(_id) if _id else None  # Ensure id is stored as a string
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)  # Ensure Flask-Login can retrieve the user ID correctly

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})  # Convert to ObjectId
        if not user_data:
            return None
        return User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])
    except:
        return None  # Handle invalid ObjectId format

# Home Route
@app.route('/test_connection')
def test_connection():
    try:
        # 强制触发一次真正的服务器握手
        info = mongo.cx.server_info()
        return f"Connected successfully! Server info: {info}"
    except Exception as e:
        return f"Failed to connect: {e}"

        return f"DB error: {e}"

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username already exists
        if mongo.db.users.find_one({"username": username}):
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        user = User(username, email, None)
        user.set_password(password)
        
        # Insert user and retrieve the _id
        inserted_user = mongo.db.users.insert_one({
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash
        })

        user.id = str(inserted_user.inserted_id)  # Assign the correct _id
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = mongo.db.users.find_one({"username": username})

        if user_data:
            user = User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Dashboard Route (Protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Profile Route
import base64

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # 获取产品表单信息
        product_image = request.files.get('product_image')
        description = request.form.get('description')
        price = request.form.get('price')
        delivery_location = request.form.get('delivery_location')
        inventory = request.form.get('inventory')
        tag = request.form.get('tag')

        image_data = None
        image_type = None
        if product_image and allowed_file(product_image.filename):
            # 获取图片的 MIME 类型，例如 "image/png"
            image_type = product_image.mimetype  
            raw_bytes = product_image.read()  # 读取文件内容到内存
            image_data = base64.b64encode(raw_bytes).decode('utf-8') 

        # 构造产品文档，并加入当前用户信息
        product = {
            "username": current_user.username,   # 记录发布该产品的用户名
            "description": description,
            "price": price,
            "delivery_location": delivery_location,
            "inventory": inventory,
            "tag": tag,
            "image_data": image_data,   # Base64 编码后的图片
            "image_type": image_type    # 图片的 MIME 类型，例如 "image/png"
        }
        mongo.db.products.insert_one(product)
        flash("Product posted successfully!", "success")
        return redirect(url_for('profile'))
    
    # GET 请求：将当前用户传递给模板
    return render_template('profile.html', user=current_user)


# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
