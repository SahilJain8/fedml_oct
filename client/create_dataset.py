import tensorflow as tf
import numpy as np
from PIL import Image


IMG_SIZE = (224, 224)
BATCH_SIZE = 32



def preprocess_image(image):
 
    img = Image.open(image)
    
   
    img = img.resize(IMG_SIZE)
    
 
    img_array = np.array(img)
    

    img_array = img_array / 255.0
    
    return img_array


def create_dataset(images):
  
    image_arrays = [preprocess_image(image) for image in images]
    

    dataset = tf.data.Dataset.from_tensor_slices(image_arrays)
    
    
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.shuffle(buffer_size=len(image_arrays))
    
    return dataset


def train_model(class1_images,class2_images,class3_images,class4_images):
    class1_dataset = create_dataset(class1_images)
    class2_dataset = create_dataset(class2_images)
    class3_dataset = create_dataset(class3_images)
    class4_dataset = create_dataset(class4_images)
