import tensorflow as tf
import numpy as np
from keras.preprocessing.image import ImageDataGenerator


IMG_SIZE = (224, 224)
BATCH_SIZE = 32


classes = ['class1', 'class2', 'class3', 'class4']


image_data_generator = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)


def preprocess_image(image):
   
    img = tf.io.decode_image(image.read(), channels=3)
   
    img = tf.image.resize(img, IMG_SIZE)
 
    img = tf.cast(img, tf.float32) / 255.0
    return img.numpy()


def create_dataset(image_lists, subset):

    image_label_pairs = []
    for class_index, image_list in enumerate(image_lists):
        for image in image_list:
            image_label_pairs.append((preprocess_image(image), class_index))
    

    np.random.shuffle(image_label_pairs)
    
    
    images = [pair[0] for pair in image_label_pairs]
    labels = [pair[1] for pair in image_label_pairs]
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))
    

    dataset = dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    
    return dataset



