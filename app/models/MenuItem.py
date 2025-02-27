from app import db

def get_mongo():
    return db  

# prevent circular imports
def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client.my_database

class MenuItem:

    @staticmethod
    def create_item(id, name, description, category, price, ingredients):

        get_mongo().db.menu_items.insert_one({
            'item_id': id, 
            'name': name, 
            'description': description, 
            'category': category,
            'price': price,
            'ingredients': ingredients,
            'quantity': 0,
            'total': 0
            })

    @staticmethod
    def find_by_id(id):
        return get_mongo().db.menu_items.find_one({'item_id': id})
    
    @staticmethod
    def find_price_by_id(id):
        item = get_mongo().db.menu_items.find_one({'item_id': id})
        if item:
            return item.get('price')
    
    @staticmethod
    def query_search(query):
        query_words = [word for word in query.split()]

        return get_mongo().db.menu_items.find({
            '$or': [
                {'name': {'$regex': '|'.join(query_words), '$options': 'i'}, 
                'description': {'$regex': '|'.join(query_words), '$options': 'i'},
                'category': {'$regex': '|'.join(query_words), '$options': 'i'}}
                ]
            })
    
    @staticmethod
    def find_by_category(category):
        return get_mongo().db.menu_items.find({'category': category})
        