import flask_pymongo
import config

# Initialize MongoDB
mongo = flask_pymongo.PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = config.DSN
    mongo.init_app(app)

# Create a user and store the data into database
def create_user(username, password):
    try:
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            return None

        user_data = {
            "username": username,
            "password": password,
            "order": []
        }
        return mongo.db.users.insert_one(user_data)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Authentication
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

# Return a list of current users' order ID
def find_user_order(username):
    try:
        user = mongo.db.users.find_one({"username": username})
        if not user:
            print("User not found")
            return []

        order_ids = user.get("order")
        # Find the correspond id in the orders databaed and give as a list
        orders = list(mongo.db.orders.find({"_id": {"$in": order_ids}}))
        # return [i["consumer"] for i in orders]
        return orders
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
        
# Create a order
def create_order(user_name, name, food, address, price, contact):
    try:   
        user = mongo.db.users.find_one({"username": user_name})
        if not user:
            print("User not found")
            return None
        
        order_data = {
                "consumer": name,
                "food": food,
                "address": address,
                "price": price,
                "contact": contact
            }
        
        order_result = mongo.db.orders.insert_one(order_data)
        order_id = order_result.inserted_id
        
        # Store the id into the list of correspond users
        mongo.db.users.update_one({"username": user_name}, {"$push": {"order": order_id}})
        return order_result
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

from bson.objectid import ObjectId
def get_order(order_id):
    return mongo.db.orders.find_one({"_id": ObjectId(order_id)})

def update_order(order_id, updated_data):
    try:
        order_object_id = ObjectId(order_id) 
        result = mongo.db.orders.update_one({"_id": order_object_id}, {"$set": updated_data})
        return result

    except Exception as e:
        raise Exception(f"Error updating order: {str(e)}")

def delete_order(order_id):
    try:
        order_object_id = ObjectId(order_id)
        result = mongo.db.orders.delete_one({"_id": order_object_id})
        return result

    except Exception as e:
        raise Exception(f"Error deleting order: {str(e)}")

def search_orders(username, search_keyword):
    try:
        user = mongo.db.users.find_one({"username": username})
        if not user:
            print("User not found")
            return []
        else:
            order_ids = user.get("order")
            orders = list(mongo.db.orders.find(
                {"_id": {"$in": order_ids}, 
                 "consumer": {"$regex": search_keyword, 
                "$options": "i"}}))
            return orders

    except Exception as e:
        print(f"Unexpected error: {e}")