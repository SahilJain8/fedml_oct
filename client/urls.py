
from django.urls import path
from .views import IndexView,upload

urlpatterns = [
   
    path("",IndexView.as_view()),
    path("image/",upload)
   
    
   
   
]