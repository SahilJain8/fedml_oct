from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ImageUploadForm
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import numpy as np




class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from the server")
def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cnv_image = form.cleaned_data['cnv_image']
            dme_image = form.cleaned_data['dme_image']
            drusen_image = form.cleaned_data['drusen_image']
            normal_image = form.cleaned_data['normal_image']

            # Convert images to numpy arrays
            cnv_image = np.array(Image.open(io.BytesIO(cnv_image.read())))
            dme_image = np.array(Image.open(io.BytesIO(dme_image.read())))
            drusen_image = np.array(Image.open(io.BytesIO(drusen_image.read())))
            normal_image = np.array(Image.open(io.BytesIO(normal_image.read())))

            # Resize the images to 224x224
            cnv_image = tf.image.resize(cnv_image, (224, 224))
            dme_image = tf.image.resize(dme_image, (224, 224))
            drusen_image = tf.image.resize(drusen_image, (224, 224))
            normal_image = tf.image.resize(normal_image, (224, 224))

            # Normalize the images
            cnv_image = cnv_image / 255.0
            dme_image = dme_image / 255.0
            drusen_image = drusen_image / 255.0
            normal_image = normal_image / 255.0

            # Create labels for the images
            cnv_label = np.array([0])
            dme_label = np.array([1])
            drusen_label = np.array([2])
            normal_label = np.array([3])

            # Create TensorFlow datasets for each image
            cnv_dataset = tf.data.Dataset.from_tensor_slices((cnv_image, cnv_label))
            dme_dataset = tf.data.Dataset.from_tensor_slices((dme_image, dme_label))
            drusen_dataset = tf.data.Dataset.from_tensor_slices((drusen_image, drusen_label))
            normal_dataset = tf.data.Dataset.from_tensor_slices((normal_image, normal_label))

            # Combine the datasets into a single dataset
            dataset = cnv_dataset.concatenate(dme_dataset).concatenate(drusen_dataset).concatenate(normal_dataset)
            dataset = dataset.shuffle(buffer_size=4)
            dataset = dataset.batch(batch_size)

            # Print the dataset
            for batch in dataset:
                print(batch)

            # Return response
            return HttpResponse("Successfully uploaded images.")
    else:
        form = ImageUploadForm()
    return render(request, 'client/upload.html', {'form': form})