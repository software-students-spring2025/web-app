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
        # only allow one cart per customer
        cart = get_mongo().carts.find_one({'customer_id': customer_id})
        if not cart:
            get_mongo().carts.insert_one({'customer_id': customer_id, 'items': [], 'total_price': 0})
            cart = get_mongo().carts.find_one({'customer_id': customer_id})

        # cart should have total price 0 if empty
        if len(cart.get('items')) == 0:
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$set': {'total_price' : 0}})
        return cart

    @staticmethod
    def add_to_cart(customer_id, item_id):
        # make sure cart exists
        cart = Cart.get_cart(customer_id)
        items = cart.get('items')

        # add item into cart ONLY if item exists
        item = get_mongo().menu_items.find_one({'item_id': item_id})
        # print("MENU ITEMS LIST: ", list(get_mongo().menu_items.find()))
        if item:
            #print("ITEM EXISTS")
            '''
            # removing to decouple item quantity from item

            if item_id in items: 
                get_mongo().menu_items.update_one({'item_id': item_id}, {'$inc': {'quantity': 1}})
                get_mongo().menu_items.update_one({'item_id': item_id}, {'$inc': {'total': item.get('price')}})
            else:
                get_mongo().carts.update_one({'customer_id': customer_id}, {'$push': {'items': item_id}})
                get_mongo().menu_items.update_one({'item_id': item_id}, {'$inc': {'quantity': 1}})
                get_mongo().menu_items.update_one({'item_id': item_id}, {'$set': {'total': item.get('price')}})
            '''
            item_price = item.get('price') # add item price to total
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$inc': {'total_price': item_price}})
            get_mongo().carts.update_one({'customer_id': customer_id}, {'$push': {'items': item_id}})


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
        print("ITEM COUNT: ", cart.get('items').count(item_id))
        return cart.get('items').count(item_id)

                
