"""URLs for the tjhome app."""

from django.urls import path
from tjhome import views

app_name = 'tjhome'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
]
