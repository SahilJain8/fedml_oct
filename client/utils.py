import tensorflow as tf
import os

def create_tf_dataset(data_dir, img_size, batch_size):
    AUTOTUNE = tf.data.experimental.AUTOTUNE
    classes = ['amd', 'dme', 'dr', 'cnv']
    train_ds = tf.data.Dataset.list_files(os.path.join(data_dir, '*/*'), shuffle=True)
    train_ds = train_ds.map(read_image, num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.map(lambda img, label: (resize_image(img, img_size), encode_label(label, classes)), num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.shuffle(buffer_size=10000)
    train_ds = train_ds.batch(batch_size)
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    return train_ds

def read_image(file_path):
    img = tf.io.read_file(file_path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img, tf.strings.split(file_path, os.path.sep)[-2]

def resize_image(img, img_size):
    img = tf.image.resize(img, [img_size, img_size])
    img /= 255.0
    return img

def encode_label(label, classes):
    one_hot = tf.one_hot(classes.index(label), len(classes))
    return one_hot
