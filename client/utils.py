import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Reshape
from django.contrib.auth.models import User
from pymongo import MongoClient
client = MongoClient('mongodb+srv://doadmin:y2Z3X0vSt4r568w7@db-mongodb-blr1-09187-cfe31e33.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-09187')
db = client['fedml']
weights_collection = db['client_model_weights']
username = " "
import uuid
unique_id = str(uuid.uuid4())
from app1.views import rms
import random as rnd

def create_image(image_byte):
    img_list = []
    for img in image_byte:
                pillow_image = Image.open(BytesIO(img.read()))
                np_array = np.array(pillow_image)
                np_array = np.resize(np_array,new_shape=(224,224))
                img_list.append(np_array)
    return img_list



def create_model(dataset):
    vgg19 = tf.keras.applications.VGG19(
    include_top = False, 
    weights = 'imagenet', 
    input_tensor = None,
    input_shape = (160,160,3), 
    pooling = None, 
    classes = 4
)
    model = tf.keras.models.Sequential([
    vgg19,
    tf.keras.layers.Conv2D(128, kernel_size = (3, 3), padding = 'same'),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Conv2D(64, kernel_size = (3, 3), padding = 'same'),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Dense(4, activation = 'softmax')
])
    model.fit(dataset.batch(32),epochs=10)
    weights_array = model.get_weights()
    username = rms()
    weights_collection.insert_one({"model_weights":weights_array[0].tobytes(),"user_name":username,"id":unique_id})



