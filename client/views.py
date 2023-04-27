from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import MultipleImagesForm
from .utils import create_image,create_model
import numpy as np
import tensorflow as tf
import threading





class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from the server")
    



def upload_images(request):
    if request.method == 'POST':
        form = MultipleImagesForm(request.POST, request.FILES)
        if form.is_valid():
            cnv_images = request.FILES.getlist('cnv_images')
            drusen_images = request.FILES.getlist('drusen_images')
            dmv_images  = request.FILES.getlist('dmv_images')
            normal_images = request.FILES.getlist('normal_images')
            cnv_data = create_image(cnv_images)
            drusen_data = create_image(drusen_images)
            normal_data = create_image(normal_images)
            dmv_data = create_image(dmv_images)
            dataset = np.concatenate([cnv_data, drusen_data, normal_data, dmv_data], axis=0)

            labels = [0] * len(cnv_data) + [1] * len(drusen_data) + [2] * len(normal_data) + [3] * len(dmv_data)

            
            dataset = tf.data.Dataset.from_tensor_slices((dataset, labels))
 
            thread = threading.Thread(target=create_model,args=(dataset,))
            thread.start()
            print("traing")



           


            return HttpResponse('Images uploaded and processed successfully.')
    else:
        form = MultipleImagesForm()
    return render(request, 'client/upload.html', {'form': form})