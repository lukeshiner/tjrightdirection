"""URLs for the hitcounter app."""

from django.urls import path

from . import views

app_name = 'hitcounter'

urlpatterns = [
    path('', views.HitCounter.as_view(), name='hit_counter'),
    path(
        'reset_trip/<int:hit_counter_id>/',
        views.ResetTrip.as_view(), name='reset_trip'),
]
