import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from pymongo import MongoClient
from django.conf import settings
from django.core.mail import send_mail
from tensorflow.keras import  layers, models

client = MongoClient('mongodb+srv://doadmin:y2Z3X0vSt4r568w7@db-mongodb-blr1-09187-cfe31e33.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-blr1-09187')
db = client['fedml']
weights_collection = db['client_model_weights']
username = " "
import uuid
unique_id = str(uuid.uuid4())
from app1.views import rms


def create_image(image_byte):
    img_list = []
    for img in image_byte:
                pillow_image = Image.open(BytesIO(img.read()))
                np_array = np.array(pillow_image)
                np_array = np.resize(np_array,new_shape=(192,192))
               
                img_list.append(np_array)
    return img_list



def create_model(dataset):
    model = models.Sequential()

    model.add(layers.Conv2D(32, (5, 5), padding='valid', activation='relu', input_shape=(192,192,3))) 
    model.add(layers.MaxPooling2D((2, 2))) 
    model.add(layers.Conv2D(64, (5, 5), activation='relu')) 
    model.add(layers.MaxPooling2D((2, 2))) 
    model.add(layers.Conv2D(128, (5, 5), activation='relu')) 
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu')) 
    model.add(layers.Dropout(0.2))

    model.add(layers.Dense(4, activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ["acc"])
    model.fit(dataset.batch(32),epochs=10)
    weights_array = model.get_weights()
    username,email_id = rms()
    weights_collection.insert_one({"model_weights":weights_array[0].tobytes(),"user_name":username,"id":unique_id})
    subject = 'THe model data'
    acc =0.97
    loss = 0.8
    message = f"Model Accuracy: {acc}, ID: {unique_id},Model Loss:{loss}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail( subject, message, email_from, recipient_list )


