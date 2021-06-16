from datetime import date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import pytz

utc=pytz.UTC

CERTIFICATE_JSON_LOCATION = '/home/auth_files/deliveryverificationservice-002943327d49.json'

class FirebaseUtils:

    def __init__(self):
        cred = credentials.Certificate(CERTIFICATE_JSON_LOCATION)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def add_document(self, collection_name, data_object):
        doc_ref = self.db.collection(collection_name).document()
        doc_ref.set(data_object)
    
    def get_order_object_from_user_id(self, collection_name, user_id):
        all_objects = self.db.collection(collection_name)
        user_orders = all_objects.where('user', '==', user_id).stream()
        total_cost = 0
        latest_order_time = pytz.UTC.localize(datetime.datetime.min)
        for order in user_orders:
            order_dict = order.to_dict()
            if latest_order_time < order_dict['time']:
                latest_order_time = order_dict['time']
                latest_order_dict = order_dict

            if order_dict['paid'] == 'no':
                total_cost += int(order_dict['cost'])
        image_location = f'http://storage.googleapis.com/milk-packet-images/{latest_order_dict["image-name"]}'
        return {
            'total-cost': total_cost,
            'image-location': image_location,
            'volume': latest_order_dict['volume'],
            'prediction': latest_order_dict['prediction'],
            'current-cost': latest_order_dict['cost']
        }

    def get_all_data(self, collection_name):
        all_data = {}
        docs = self.db.collection(collection_name).stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            if 'prediction' in doc_dict:
                all_data[str(doc.id)] = doc_dict['prediction']
        return all_data