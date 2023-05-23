from pymongo import MongoClient
import numpy as  np
import tensorflow as tf

# Define your model architecture
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


def fedagg(request):
    average_weights = np.mean(model_weights_list, axis=0)
    model = my_model()

    model.set_weights(average_weights)

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    model.save('trained_model.h5')