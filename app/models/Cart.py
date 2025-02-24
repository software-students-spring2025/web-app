from app import mongo
'''
doc in progress:
contains all items, keeps track of total price of items in cart
Every customer gets only one cart, unique identifier is customerID
'''

class Cart:

    @staticmethod
    def createCart(customerID):
        # only allow one cart per customer
        if not mongo.db.carts.find_one({'customerID': customerID}):
            mongo.db.carts.insert_one({'customerID': customerID, 'items': [], 'totalPrice': 0})

    @staticmethod
    def addToCart(customerID, itemID):

        # make sure cart exists
        Cart.createCart(customerID)

        # add item into cart ONLY if item exists
        item = mongo.db.items.find_one({'itemID': itemID})
        if item:
            mongo.db.carts.update_one({'customerID': customerID}, {'$push': {'items': itemID}})
            itemPrice = item.get('price') # add item price to total
            mongo.db.carts.update_one({'customerID': customerID}, {'$inc': {'totalPrice': itemPrice}})


    @staticmethod
    def removeFromCart(customerID, itemID):

        cart = mongo.db.carts.find_one({'customerID': customerID})

        # make sure cart exists
        if not cart:
            return
        
        items = cart.get('items')

        # remove single instance of item if it exists
        if itemID in items:
            items.remove(itemID)
            item = mongo.db.items.find_one({'itemID': itemID})
            if item: # subtract item price from total
                itemPrice = item.get('price')
                mongo.db.carts.update_one({'customerID': customerID}, {'$inc': {'totalPrice': -itemPrice}})

            mongo.db.carts.update_one({'customerID': customerID}, {'$set': {'items': items}})



    @staticmethod
    def calculateRawTotal(customerID):
        cart = mongo.db.carts.find_one({'customerID': customerID})
        # reset price
        totalPrice = 0
                                  
        if not cart:
            return
        items = cart.get('items')

        for itemID in items:
            item = mongo.db.items.find_one({'itemID': itemID})
            if item:
                itemPrice = item.get('price')
                totalPrice += itemPrice
            else:
                # invalid item
                mongo.db.carts.update_one({'customerID': customerID}, {'$pull': {'items': itemID}})

        mongo.db.carts.update_one({'customerID': customerID}, {'$set': {'totalPrice': totalPrice}})
        return totalPrice

                
