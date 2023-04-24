from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
def upload(request):
    if request.method =="POST":
            class1_images = request.FILES.getlist('class1[]')
            class2_images = request.FILES.getlist('class2[]')
            class3_images = request.FILES.getlist('class3[]')
            class4_images = request.FILES.getlist('class4[]')
            return HttpResponse("Image upload succesfully")
            
    return render(request,"upload.html")