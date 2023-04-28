
from django.urls import path
from .views import IndexView,upload_images,oct

urlpatterns = [
   
    path("index",IndexView.as_view(),name='home'),
    path("image/",upload_images,name="upload_image"),
    path("oct/",oct,name="oct"),
   
   
    
   
   
]