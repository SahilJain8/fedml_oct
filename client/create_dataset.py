import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the image size and batch size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32


classes = ['class1', 'class2', 'class3', 'class4']


image_data_generator = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Define a function to create a dataset from a list of images
def create_dataset(image_lists, subset):
    # Create a list of (image, label) pairs
    image_label_pairs = []
    for class_index, image_list in enumerate(image_lists):
        for image in image_list:
            image_label_pairs.append((image, class_index))
    
   
    np.random.shuffle(image_label_pairs)
    
   
    image_paths = [pair[0] for pair in image_label_pairs]
    labels = [pair[1] for pair in image_label_pairs]
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    
  
    generator = image_data_generator.flow_from_dataframe(
        dataframe=tf.data.Dataset.zip((dataset, tf.data.Dataset.range(len(image_paths)))).shuffle(buffer_size=len(image_paths)),
        x_col=0, y_col=1,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        subset=subset
    )
    
    return generator


