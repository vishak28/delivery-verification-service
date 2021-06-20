from flask import request
from flask_api import FlaskAPI
from flask import jsonify
from flask_cors import CORS
import datetime
from firebase_utils.database import FirebaseUtils
from storage_utils.cloud_storage import StorageUtils
from cnn_model.cnn import CnnModel
from utils.calculate_utils import Utils
from utils.file_utils import FileUtils


app = FlaskAPI(__name__)
CORS(app)
storage = StorageUtils()
db = FirebaseUtils()
cnn = CnnModel()
utils = Utils()
file_utils = FileUtils()

@app.route('/receiveImages', methods=['POST'])
def receiveImages():
    if request.files is None:
        return jsonify({
            'status': 'unsuccessful',
            'message': 'Upload image not found'
        })

    image_name = file_utils.save_file(request.files['upload'])
    try:
        storage.upload_blob(image_name)
    except:
        error_message = 'Error while uploading image to storage'
        print(error_message)
        return jsonify({
            'status': 'unsuccessful',
            'message': error_message
        })
    return jsonify({
        'status': "success",
        'image-name': image_name
        })


@app.route('/getAllData', methods=['GET'])
def getAllData():
    print('fetching all data')
    data = db.get_all_data('milk-data')
    return jsonify(data)

@app.route('/getorderinfo', methods=['POST'])
def getOrderInfo():
    data = request.get_json()
    user_id = data['user_id']
    response = db.get_order_object_from_user_id('milk-data', user_id)
    return jsonify(response)


@app.route('/verify',methods=['POST'])
def verify():
    print("Detection started...")
    data = request.get_json()
    print(data)
    #Get data in request
    user_id = data['userId']
    time_data = datetime.datetime.now()
    weight_data = data['weight']
    volume_data = utils.calculate_volume(weight_data)
    image_name = data['image-name']
    device_data = {
            'time': time_data,
            'weight': weight_data,
            'volume': volume_data,
            'image-name': image_name,
            'paid': 'no'       
        }

    #Run the model
    try:
        prediction_result = cnn.classify(image_name)
        cost_data = utils.calculate_cost(prediction_result, volume_data)
    except:
        return jsonify({
            'status': "unsuccessful",
            "user":user_id,
            "type":"Error"
            })
    
    #Yeet downloaded file
    file_utils.delete_file(image_name)

    #Send response
    device_data['prediction'] = prediction_result
    device_data['cost'] = cost_data
    db.add_order('user-data', user_id, device_data)
    return jsonify({
        'status': "success",
        "user":user_id,
        "type":prediction_result
        })


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080)




