from django.shortcuts import render
from django.http import HttpResponse
from .create_dataset import create_dataset

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
def upload(request):
    if request.method =="POST":
            image_lists = [
    request.FILES.getlist('class1[]'),
    request.FILES.getlist('class2[]'),
    request.FILES.getlist('class3[]'),
    request.FILES.getlist('class4[]')
]

          
            
            dataset = create_dataset(image_lists)
            print(dataset)
            


            return HttpResponse("Image upload succesfully")
            
    return render(request,"upload.html")