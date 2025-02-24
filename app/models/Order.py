from app import mongo
'''
Order record with payment information, can be accessed later
Currently orderID is just the number order it is, discuss to change
'''

class Order:
    order_count = 0
    shipping_price = 2 # 2 dollars shipping price, could make it tied to location?
    
    @staticmethod
    def create_order(cart, customerID, totalPrice, paymentInfo, shipping, shippingAddress = None):
        Order.order_count += 1
        # tax and shipment
        tax = totalPrice * 0.085
        totalPrice += tax
        totalPrice += Order.shipping_price * shipping # make this tied to location?

        mongo.db.orders.insert_one({
            'orderID': Order.order_count, 
            'customerID': customerID,
            'items': cart, 
            'totalPrice': totalPrice,
            'tax': tax,
            'paymentInfo': paymentInfo, 
            'shipping': shipping,
            'shippingAddress': shippingAddress #geolocation feature?
            })
        
    

        