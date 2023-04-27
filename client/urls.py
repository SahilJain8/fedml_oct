
from django.urls import path
from .views import IndexView,upload_images

urlpatterns = [
   
    path("",IndexView.as_view()),
    path("image/",upload_images)
   
    
   
   
]