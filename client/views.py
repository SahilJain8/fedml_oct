from django.http import HttpResponse
from django.views import View
import os
import numpy as np
from PIL import Image
from django.shortcuts import render
from .forms import MultiCategoryImageForm






class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from the server")


import os
import numpy as np
from PIL import Image
from django.shortcuts import render
from .forms import MultiCategoryImageForm

def upload_images(request):
    if request.method == 'POST':
        form = MultiCategoryImageForm(request.POST, request.FILES)
        if form.is_valid():
            # create a dataset
            dataset = []
            for category in form.CATEGORY_CHOICES:
                category_images = request.FILES.getlist(f'{category[0]}_images')
                for img_file in category_images:
                    img = Image.open(img_file)
                    img_array = np.array(img)
                    dataset.append((img_array, category[0]))
            
            # do something with the dataset here
            # ...
            
            return render(request, 'result.html')
    else:
        form = MultiCategoryImageForm()
    return render(request, 'upload.html', {'form': form})

