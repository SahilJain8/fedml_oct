from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
def upload(request):
    if request.method =="POST":
        image = request.FILES.get('images')
        print(image)
    return render(request,"upload.html")