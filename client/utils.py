import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Reshape
from django.contrib.auth.models import User
from pymongo import MongoClient
client = MongoClient('mongodb+srv://root:6u1jPRiUjEY7G4tx@cluster0.chilgc4.mongodb.net/test')
db = client['fedml_cor']
weights_collection = db['client_client_model_weights']
username = " "
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
    model = Sequential([
        Reshape((224, 224, 1), input_shape=(224, 224)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    model.fit(dataset.batch(32),epochs=10)
    weights_array = model.get_weights()
    username = rms()
    print(username)
    user = User.objects.get(username=username)
    user_id = user.id
    print(username)
    weights_collection.insert_one({"model_weights":weights_array[0].tobytes(),"user_name":username,"id":rnd.random(10,10000)})



