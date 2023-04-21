from django.contrib import admin
from django.urls import path
from .views import index,FLwrView

urlpatterns = [
    path('', index),
    path('server/',FLwrView.as_view())
]
