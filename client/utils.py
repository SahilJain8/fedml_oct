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
   
    model.compile(optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
    return model



client = MongoClient('mongodb+srv://doadmin:y2Z3X0vSt4r568w7@db-mongodb-blr1-09187-cfe31e33.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-09187')
db = client['fedml']
weights_collection = db['client_model_weights']
documents = weights_collection.find()

model_weights_list = []

for document in documents:
    model_weights_bytes = document['model_weights']
    model_weights_np = eval(model_weights_bytes)
    model_weights_np = np.array(model_weights_np)
    model_weights_list.append(model_weights_np)


def fedagg():
    average_weights = np.mean(model_weights_list, axis=0)
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
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])


   
    model.save('model.h5')





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
    history = model.fit(dataset.batch(32),epochs=10)
    accuracy_history = history.history['accuracy']

    weights_array = model.get_weights()
    username,email_id = rms()
    weights_collection.insert_one({"model_weights":str(weights_array[0].tolist()),"user_name":username,"id":unique_id})
    subject = 'THe model data'

    loss = 0.8
    message = f"Model Accuracy: {accuracy_history[9]} \n, ID: {unique_id},\nModel Loss:{loss}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail( subject, message, email_from, recipient_list )
    fedagg()
   

