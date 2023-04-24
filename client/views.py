from django.shortcuts import render
from django.http import HttpResponse
from .create_dataset import create_dataset

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
            class1_dataset = create_dataset(class1_images)
            class2_dataset = create_dataset(class2_images)
            class3_dataset = create_dataset(class3_images)
            class4_dataset = create_dataset(class4_images)
            print(class1_dataset)


            return HttpResponse("Image upload succesfully")
            
    return render(request,"upload.html")