from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . views import *

urlpatterns = [
    # path("", views.home, name="home"),
    path("", views.dashboard, name="dashboard"),
    path("scraped_data/", views.scraped_data, name="scraped_data"),
    path("download_and_save/", views.download_and_save, name="download_and_save"),
    
]
   

