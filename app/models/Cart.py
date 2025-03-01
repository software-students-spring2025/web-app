from app import db

def get_mongo():
    return db 
     
'''
doc in progress:
contains all items, keeps track of total price of items in cart
Every customer gets only one cart, unique identifier is customerID

'''

class Cart:

    @staticmethod
    def get_cart(customer_id):
        cart = get_mongo().carts.find_one({'customer_id': customer_id})
        if cart:
            cart['_id'] = str(cart['_id'])
            item_counts = {}
            for item_id in cart['items']:
                item_counts[item_id] = item_counts.get(item_id, 0) + 1
        else:
            get_mongo().carts.insert_one({'customer_id': customer_id, 'items': [], 'total_price': 0})
            cart = get_mongo().carts.find_one({'customer_id': customer_id})
            cart['_id'] = str(cart['_id'])
        return cart


    @staticmethod
    def add_to_cart(customer_id, item_id):
        # make sure cart exists
        cart = Cart.get_cart(customer_id)
        # add item into cart ONLY if item exists
        item = get_mongo().menu_items.find_one({'item_id': item_id})
        if item:
            #print("ITEM EXISTS")

            item_price = item.get('price') # add item price to total
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$inc': {'total_price': item_price}})
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$push': {'items': item_id}})

            from flask import session
            if 'cart' not in session:
                session['cart'] = {}
            if item_id in session['cart']:
                session['cart'][item_id] += 1
            else:
                session['cart'][item_id] = 1
            session.modified = True


    @staticmethod
    def remove_from_cart(customer_id, item_id):

        cart = get_mongo().carts.find_one({'customer_id': customer_id})

        # make sure cart exists
        if not cart:
            return
        
        items = cart.get('items')

        # remove single instance of item if it exists
        if item_id in items:
            items.remove(item_id)
            item = get_mongo().menu_items.find_one({'item_id': item_id})
            if item: # subtract item price from total
                item_price = item.get('price')
                get_mongo().carts.update_one({'customer_id': customer_id}, {'$inc': {'total_price': -item_price}})
            
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$set': {'items': items}})

            from flask import session
            if 'cart' in session and item_id in session['cart']:
                session['cart'][item_id] -= 1
                if session['cart'][item_id] <= 0:
                    del session['cart'][item_id]
                session.modified = True



    @staticmethod
    def calculate_raw_total(customer_id):
        cart = get_mongo().carts.find_one({'customer_id': customer_id})
        # reset price
        total_price = 0
                                  
        if not cart:
            return
        items = cart.get('items')

        for item_id in items:
            item = get_mongo().menu_items.find_one({'item_id': item_id})
            if item:
                item_price = item.get('price')
                total_price += item_price
            else:
                # invalid item
                get_mongo().carts.update_one({'customer_id': customer_id}, {'$pull': {'items': item_id}})

        get_mongo().carts.update_one({'customer_id': customer_id}, {'$set': {'total_price': total_price}})
        return total_price


    @staticmethod
    def get_item_count(customer_id, item_id):
        cart = get_mongo().carts.find_one({'customer_id': customer_id})
        # reset price
        total_price = 0
                                  
        if not cart:
            return
        return cart.get('items').count(item_id)

    @staticmethod
    def clear_cart(customer_id, item_id):
        get_mongo().carts.delete_many({'customer_id': customer_id})
        return Cart.get_cart(customer_id)

    @staticmethod
    def clear_cart(customer_id):
        get_mongo().carts.delete_many({'customer_id': customer_id})
        return Cart.get_cart(customer_id)
                