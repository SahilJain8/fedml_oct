import tensorflow as tf
import numpy as np
from PIL import Image


IMG_SIZE = (150, 150)
BATCH_SIZE = 32


classes = ['Choroidal neovascularization', 'Diabetic macular edema', 'Optic disc drusen ', 'Normal ']


def create_dataset(image_lists):
    
    IMG_HEIGHT = 150
    IMG_WIDTH = 150


    labels = [0]*len(image_lists[0]) + [1]*len(image_lists[1]) + [2]*len(image_lists[2]) + [3]*len(image_lists[3])

   
    images = []
    for img_list in image_lists:
        images += img_list

 
    def preprocess_image(image):
     
        image = tf.image.convert_image_dtype(image, tf.float32)
     
        image = tf.image.resize(image, [IMG_HEIGHT, IMG_WIDTH])
        return image

  
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))

    dataset = dataset.map(lambda x, y: (preprocess_image(x), y))
    
    return dataset
