import flask_pymongo
import config

# Initialize MongoDB
mongo = flask_pymongo.PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = config.DSN
    mongo.init_app(app)

def create_user(username, password):
    try:
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            return None

        user_data = {
            "username": username,
            "password": password,
        }
        return mongo.db.users.insert_one(user_data)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def login_user(username, password):
    try:
        user = mongo.db.users.find_one({"username": username})
        print(user["password"])

        if user and user["password"] == password:
            return user
        else:
            return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

