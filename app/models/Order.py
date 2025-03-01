from app import db

def get_mongo():
    return db 

from .Cart import Cart

'''
Order record with payment information, can be accessed later
Currently orderID is just the number order it is, discuss to change
'''

class Order:
    order_count = 0
    shipping_price = 2 # 2 dollars shipping price, could make it tied to location?
    
    @staticmethod
    def submit_order(customer_id, first_name, last_name, email, card_number, cvv, zip_code, delivery_method, shipping_address = 'N/A'):
        Order.order_count += 1
        # tax and shipment
        order_id = Order.order_count

        cart = Cart.get_cart(customer_id)
        total_price = Cart.calculate_raw_total(customer_id)

        '''
        tax = total_price * 0.085
        total_price += tax
        total_price += Order.shipping_price * (delivery_method == 'delivery') # make this tied to location?
        '''
        tax = 0

        total_price = round(total_price, 2)

        last_four = card_number[-4:]

        item_ids = cart.get('items', [])
        print("CART ORDER ITEMS: ", item_ids)
        
        items = []

        for item_id in sorted(list(set(item_ids))):
            item = get_mongo().menu_items.find_one({'item_id': item_id})
            if item and Cart.get_item_count(customer_id, item_id) > 0:
                item['quantity'] = Cart.get_item_count(customer_id, item_id)
                item['total'] = Cart.get_item_count(customer_id, item_id) * item.get('price')
                items.append(item)

        get_mongo().orders.insert_one({
            'order_id': order_id, 
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'card_number': card_number,
            'last_four': last_four,
            'cvv': cvv,
            'zip_code': zip_code,
            'items': items, 
            'total_price': total_price,
            'tax': tax,
            'delivery_method': delivery_method
            })

        print("CART ITEMS IN ORDER: ", cart.get('items'))

        if delivery_method == 'delivery':
            get_mongo().orders.update_one({'order_id': order_id, 'customer_id': customer_id}, {'$set': {'shipping_address': shipping_address}})
        else:
            get_mongo().orders.update_one({'order_id': order_id, 'customer_id': customer_id}, {'$set': {'shipping_address': 'N/A'}})

        Cart.clear_cart(customer_id)

    @staticmethod
    def delete_order(order_id, customer_id):
        get_mongo().orders.delete_many({'order_id': int(order_id), 'customer_id': customer_id})

    @staticmethod
    def view_orders(customer_id):
        orders = get_mongo().orders.find({'customer_id': customer_id})
        order_info = []
        for order in orders:
            order = {
                'order_id': order.get('order_id'),
                'first_name': order.get('first_name', ''),
                'last_name': order.get('last_name', ''),
                'email': order.get('email', ''),
                'items': order.get('items', ''),
                'total_price': order.get('total_price', 0.0),
                'delivery_method': order.get('delivery_method'),
                'shipping_address': order.get('shipping_address', 'N/A'),
                'last_four': order.get('last_four', '0000')
            }
            order_info.append(order)
        return order_info