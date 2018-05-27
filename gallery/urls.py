"""URLs for the gallery app."""

from django.urls import path
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('', views.Gallery.as_view(), name='gallery'),
]
