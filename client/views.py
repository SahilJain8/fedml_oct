from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import MultipleImagesForm
from .utils import create_image,create_model
import numpy as np
import tensorflow as tf
import threading
from django.shortcuts import render
import tensorflow as tf
import numpy as np
from tensorflow import keras
from PIL import Image
from io import BytesIO
model=keras.models.load_model("client/model.h5")
classes_name={0:"Choroidal neovascularization",1:"Diabetic macular edema ",2:"Drusen",3:"Normal"}

class IndexView(View):
    def get(self, request):
        return render(request,"index.html")
    



async def upload_images(request):
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
            threading.Thread(target=create_model,args=(dataset,)).start()
            return render(request,"index.html")

        
    else:
        form = MultipleImagesForm()
    return render(request, 'client/upload.html', {'form': form})


def oct(request):
    if request.method == "POST":
            img_data = request.FILES['image'].read()
            img = Image.open(BytesIO(img_data))
            image= img.resize((160,160))
            image = np.expand_dims(image, axis=0)
            image=image/255.
            predection=model.predict(image)
            pre=predection.flatten()
            m=pre.max()
            pre=list(pre)
            context = {'prediction': str(classes_name[pre.index(m)])  }
    
            return render(request, 'oct.html', context)

    return render(request,"oct.html")