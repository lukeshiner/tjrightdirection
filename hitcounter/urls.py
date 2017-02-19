from django.conf.urls import url

from . import views

app_name = 'hitcounter'

urlpatterns = [
    url(r'^$', views.hit_counter, name='hit_counter'),
    url(
        r'^reset_trip/(?P<hit_counter_id>[0-9]+)/$',
        views.reset_trip, name='reset_trip'),
]
