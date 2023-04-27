from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
from io import BytesIO
import tensorflow as tf
class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from the server")
    



def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cnv_image = form.cleaned_data['cnv_image'].read()
            dme_image = form.cleaned_data['dme_image']
            drusen_image = form.cleaned_data['drusen_image']
            normal_image = form.cleaned_data['normal_image']
            image_list = [    (cnv_image, 0),    (dme_image, 1),    (drusen_image, 2),    (normal_image, 3)]
            print(len(cnv_image))


            # Return response
            return HttpResponse("Successfully uploaded images.")
    else:
        form = ImageUploadForm()
    return render(request, 'client/upload.html', {'form': form})
