import os
import tensorflow as tf
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm


# Define the image shape and number of classes
IMG_SHAPE = (224, 224, 3)
NUM_CLASSES = 4


def create_tf_dataset(images):
    # Convert images to TensorFlow dataset
    dataset = tf.data.Dataset.from_tensor_slices(images)
    # Resize and normalize images
    def preprocess_image(image):
        image = tf.image.resize(image, IMG_SHAPE[:2])
        image = tf.cast(image, tf.float32)
        image /= 255.0
        return image
    dataset = dataset.map(preprocess_image)
    return dataset


def train_model(images):
    # Create the TensorFlow dataset
    dataset = create_tf_dataset(images)
    
    # Load the pre-trained model and freeze its layers
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, include_top=False, weights="imagenet")
    base_model.trainable = False

    # Add a new output layer for the number of classes
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    output = tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    # Create the model and compile it
    model = tf.keras.models.Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"])

    # Train the model
    model.fit(dataset, epochs=10)

    return model


@csrf_exempt
async def upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded images
            class_1_images = request.FILES.getlist("class_1_images")
            class_2_images = request.FILES.getlist("class_2_images")
            class_3_images = request.FILES.getlist("class_3_images")
            class_4_images = request.FILES.getlist("class_4_images")
            
            # Combine the images and create labels
            images = []
            labels = []
            for img in class_1_images:
                images.append(img)
                labels.append([1, 0, 0, 0])
            for img in class_2_images:
                images.append(img)
                labels.append([0, 1, 0, 0])
            for img in class_3_images:
                images.append(img)
                labels.append([0, 0, 1, 0])
            for img in class_4_images:
                images.append(img)
                labels.append([0, 0, 0, 1])
            
            # Train the model
            model = await asyncio.to_thread(train_model, images)

            # Return a success response
            return JsonResponse({"success": True})
    else:
        form = ImageForm()
    return render(request, "upload.html", {"form": form})
