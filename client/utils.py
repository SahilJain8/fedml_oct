import cv2
import numpy as np
from PIL import Image
from io import BytesIO




def create_image(image_byte):
    img_list = []
    for img in image_byte:
                pillow_image = Image.open(BytesIO(img.read()))
                np_array = np.array(pillow_image)
                np_array = np.resize(np_array,new_shape=(224,224))
                img_list.append(np_array)
    return img_list