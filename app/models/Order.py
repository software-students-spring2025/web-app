from pymongo import MongoClient

# prevent circular imports
def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client.my_database

'''
Order record with payment information, can be accessed later
Currently orderID is just the number order it is, discuss to change
'''

class Order:
    order_count = 0
    shipping_price = 2 # 2 dollars shipping price, could make it tied to location?
    
    @staticmethod
    def create_order(cart, customer_id, total_price, payment_info, shipping, shipping_address = None):
        Order.order_count += 1
        # tax and shipment
        tax = total_price * 0.085
        total_price += tax
        total_price += Order.shipping_price * shipping # make this tied to location?

        get_mongo().db.orders.insert_one({
            'orderID': Order.order_count, 
            'customerID': customer_id,
            'items': cart, 
            'total_price': total_price,
            'tax': tax,
            'payment_info': payment_info, 
            'shipping': shipping,
            'shippingAddress': shipping_address #geolocation feature?
            })
        
    

        