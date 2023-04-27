import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Reshape



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

    model.fit(dataset.batch(32), epochs=10)

