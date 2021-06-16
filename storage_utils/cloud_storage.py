
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/auth_files/deliveryverificationservice-002943327d49.json"

BUCKET_NAME = 'milk-packet-images'

class StorageUtils:

    def __init__(self):
        storage_client = storage.Client()
        self.bucket = storage_client.bucket(BUCKET_NAME)

    def upload_blob(self, source_file_name):
        blob = self.bucket.blob(source_file_name)
        blob.upload_from_filename(source_file_name)
        print(
            "File {} uploaded to {}.".format(
                source_file_name, source_file_name
            )
        )
