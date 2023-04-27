import tensorflow as tf
import numpy as np
from PIL import Image
import io
def load_image_from_memory(image_bytes):
    # Load image from bytes and convert to numpy array
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)
    # Normalize pixel values to be between 0 and 1
    image_array = image_array / 255.0
    return image_array



def create_dataset(cnv_image_list, dme_image_list, drusen_image_list, normal_image_list, cnv_label_list, dme_label_list, drusen_label_list, normal_label_list, batch_size=32):
    # Load image data from memory
    cnv_image_array = np.stack([load_image_from_memory(image_bytes) for image_bytes in cnv_image_list], axis=0)
    dme_image_array = np.stack([load_image_from_memory(image_bytes) for image_bytes in dme_image_list], axis=0)
    drusen_image_array = np.stack([load_image_from_memory(image_bytes) for image_bytes in drusen_image_list], axis=0)
    normal_image_array = np.stack([load_image_from_memory(image_bytes) for image_bytes in normal_image_list], axis=0)

    # Create a numpy array of labels

    labels = np.array([cnv_label_list, dme_label_list, drusen_label_list, normal_label_list])

    # Create a TensorFlow dataset from the image and label arrays
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))
    dataset = dataset.batch(batch_size)

    return dataset

        

