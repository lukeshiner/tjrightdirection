"""URLs for the recomendations app."""

from django.urls import path
from recomendations import views

app_name = 'recomendations'

urlpatterns = [
    path('', views.Recomendations.as_view(), name='recomendations'),
]
