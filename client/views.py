from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ImageUploadForm
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import numpy as np


# dataset = tf.data.Dataset.from_tensor_slices((images, labels))

# # Shuffle and batch the dataset
# dataset = dataset.shuffle(buffer_size=len(images))
# dataset = dataset.batch(batch_size)


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
            cnv_image = np.array(Image.open(io.BytesIO(cnv_image.read())))
            dme_image = np.array(Image.open(io.BytesIO(dme_image.read())))
            drusen_image = np.array(Image.open(io.BytesIO(drusen_image.read())))
            normal_image = np.array(Image.open(io.BytesIO(normal_image.read())))

            images = np.stack([cnv_image, dme_image, drusen_image, normal_image], axis=0)
            labels = np.array([0, 1, 2, 3])

            # Create TensorFlow dataset
            dataset = tf.data.Dataset.from_tensor_slices((images, labels))
            dataset = dataset.shuffle(buffer_size=len(images))
            dataset = dataset.batch(32)

           
            print(dataset)

            return HttpResponse("Successfully uploaded images.")
    else:
        form = ImageUploadForm()
    return render(request, 'client/upload.html', {'form': form})
