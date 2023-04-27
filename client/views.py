from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ImageUploadForm


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
         
            return HttpResponse("Succesfully")
    else:
        form = ImageUploadForm()
    return render(request, 'client/upload.html', {'form': form})

