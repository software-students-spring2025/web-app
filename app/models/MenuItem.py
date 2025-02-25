from app import mongo


class MenuItem:

    @staticmethod
    def createItem(id, name, description, category, price, ingredients):

        mongo.db.items.insert_one({
            'itemID': id, 
            'name': name, 
            'description': description, 
            'category': category,
            'price': price,
            'ingredients': ingredients
            })

    @staticmethod
    def findByID(id):
        return mongo.db.items.find_one({'itemID': id})
    
    @staticmethod
    def findPriceByID(id):
        item = mongo.db.items.find_one({'itemID': id})
        if item:
            return item.get('price')
    
    @staticmethod
    def querySearch(query):
        queryWords = [word for word in query.split()]

        return mongo.db.items.find({
            '$or': [
                {'name': {'$regex': '|'.join(queryWords), '$options': 'i'}, 
                'description': {'$regex': '|'.join(queryWords), '$options': 'i'},
                'category': {'$regex': '|'.join(queryWords), '$options': 'i'}}
                ]
            })
    
    @staticmethod
    def findByCategory(category):
        return mongo.db.items.find({'category': category})
        