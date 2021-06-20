from datetime import date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from flask.json import jsonify
import pytz

utc=pytz.UTC

CERTIFICATE_JSON_LOCATION = '/home/auth_files/deliveryverificationservice-002943327d49.json'

class FirebaseUtils:

    def __init__(self):
        cred = credentials.Certificate(CERTIFICATE_JSON_LOCATION)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def add_order(self, collection_name, user_id, order_data):
        new_order = self.db.collection(collection_name).document(user_id).collection('order-data').document()
        new_order.set(order_data)
    
    def get_order_object_from_user_id(self, collection_name, user_id):
        all_orders = self.db.collection(collection_name).document(user_id).collection('order-data')
        user_orders = all_orders.order_by('time', direction=firestore.Query.DESCENDING).stream()
        total_cost = 0
        order_list = []
        for order in user_orders:
            order_dict = order.to_dict()
            order_list.append(order_dict)
            if order_dict['paid'] == 'no':
                total_cost += int(order_dict['cost'])
        return jsonify({
            'orderlist': order_list
        })

    def get_latest_order_object_from_user_id(self, collection_name, user_id):
        all_orders = self.db.collection(collection_name).document(user_id).collection('order-data')
        user_orders = all_orders.order_by('time', direction=firestore.Query.DESCENDING).stream()
        total_cost = 0
        order_list = []
        for order in user_orders:
            order_dict = order.to_dict()
            order_list.append(order_dict)
            if order_dict['paid'] == 'no':
                total_cost += int(order_dict['cost'])
        latest_order = order_list[0]
        return jsonify({
            'total-cost': total_cost,
            'image-location': latest_order['image-location'],
            'volume': latest_order['volume'],
            'prediction': latest_order['prediction'],
            'current-cost': latest_order['cost']
        })
