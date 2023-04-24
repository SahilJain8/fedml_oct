import tensorflow as tf
import numpy 
from keras.preprocessing.image import ImageDataGenerator, load_img



vgg19 = tf.keras.applications.VGG19(
    include_top = False, 
    weights = 'imagenet', 
    input_tensor = None,
    input_shape = (150,150,3), 
    pooling = None, 

)



vgg19.trainable = False
model_vgg = tf.keras.models.Sequential([
    
    vgg19,
    tf.keras.layers.Conv2D(128, kernel_size = (3, 3), padding = 'same'),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Conv2D(64, kernel_size = (3, 3), padding = 'same'),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100),
    tf.keras.layers.PReLU(alpha_initializer='zeros'),
    tf.keras.layers.Dense(4, activation = 'softmax')
])



model_vgg.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['acc'])


def train_ml(train_generator,validation_generator):

    history_vgg = model_vgg.fit(
        train_generator,
        steps_per_epoch = (83484/500),
        epochs = 20,
        validation_data = validation_generator,
        validation_steps = (32/16),
        max_queue_size=100,
        workers = 4 ,
        use_multiprocessing=True,
        verbose = 1)

    return model_vgg.weights()