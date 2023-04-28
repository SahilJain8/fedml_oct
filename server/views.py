
import tensorflow as tf
import tensorflow_federated as tff
from pymongo import MongoClient


client = MongoClient('mongodb+srv://root:6u1jPRiUjEY7G4tx@cluster0.chilgc4.mongodb.net/test')
db = client['fedml_cor']
collection = db["client_client_model_weights'"]
weights_document = collection.find_one({"_id": ""})
weights = tf.constant(weights_document["weights"])


def model_fn():
  model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
  ])
  loss = tf.keras.losses.CategoricalCrossentropy()
  optimizer = tf.keras.optimizers.Adam()
  return tff.learning.from_keras_model(
      model, 
      input_spec=tf.TensorSpec(shape=(None, 224, 224, 3), dtype=tf.float32), 
      loss=loss, 
      metrics=[tf.keras.metrics.CategoricalAccuracy()],
      optimizer=optimizer
  )

@tff.federated_computation
def federated_average(weights):
  return tff.learning.build_federated_averaging_process(model_fn)({weights})

iterative_process = federated_average(weights)
state = iterative_process.initialize()
for _ in range(10):
    state, metrics = iterative_process.next(state, [None])
average = state.model.trainable.variables[0]


result = {"average": average.numpy().tolist()}
collection.insert_one(result)
