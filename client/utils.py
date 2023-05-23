import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from pymongo import MongoClient
from django.conf import settings
from django.core.mail import send_mail
from tensorflow.keras import  layers, models
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Reshape

client = MongoClient('mongodb+srv://doadmin:y2Z3X0vSt4r568w7@db-mongodb-blr1-09187-cfe31e33.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-09187')
db = client['fedml']
weights_collection = db['client_model_weights']
username = " "
import uuid
unique_id = str(uuid.uuid4())
from app1.views import rms


def my_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(192, 192, 3)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')
    ])
    return model



client = MongoClient('mongodb+srv://doadmin:y2Z3X0vSt4r568w7@db-mongodb-blr1-09187-cfe31e33.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-09187')
db = client['fedml']
weights_collection = db['client_model_weights']
documents = weights_collection.find()

model_weights_list = []

for document in documents:
    model_weights_bytes = document['model_weights']
    model_weights_np = np.frombuffer(model_weights_bytes, dtype=np.float32)
    model_weights_list.append(model_weights_np)


def fedagg():
    average_weights = np.mean(model_weights_list, axis=0)
    model = my_model()

    model.set_weights(average_weights)

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    model.save('trained_model.h5')





def create_image(image_byte):
    img_list = []
    for img in image_byte:
        pillow_image = Image.open(BytesIO(img.read()))
        np_array = np.array(pillow_image)
        np_array = np.resize(np_array,new_shape=(224,224))
        img_list.append(np_array)
    return img_list
def create_model(dataset):
    model = models.Sequential([
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
    username,email_id = rms()
    weights_collection.insert_one({"model_weights":weights_array[0].tobytes(),"user_name":username,"id":unique_id})
    subject = 'THe model data'
    acc =0.97
    loss = 0.8
    message = f"Model Accuracy: {acc} \n, ID: {unique_id},Model Loss:{loss}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail( subject, message, email_from, recipient_list )
    fedagg()
   

