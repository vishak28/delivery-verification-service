import cv2
from tensorflow.keras import layers, models, regularizers
import numpy as np


IMG_SIZE = 100
CHECKPOINT_PATH = './cnn_model/trained_model/cp.ckpt'
CATEGORIES = ['NandiniBlue', 'NandiniGoodLife', 'NandiniGreen', 'NandiniOrange', 'NandiniSlim']

class CnnModel():
    
    def __init__(self):
        self.cnn = self.create_model()

    def classify(self, imgPath):
        img = cv2.imread(imgPath)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = np.array(img).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

        res = CATEGORIES[np.argmax(self.cnn.predict(img))]
        return res

    def create_model(self):
        cnn = models.Sequential([
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),

            layers.Flatten(),

            layers.Dense(
                units=32,
                kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),
                bias_regularizer=regularizers.l2(1e-4),
                activity_regularizer=regularizers.l2(1e-5)
            ),

            layers.Dense(5, activation='softmax')
        ])

        cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        cnn.load_weights(CHECKPOINT_PATH)
        return cnn
    