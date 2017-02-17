from django.conf.urls import url

from . import views

app_name = 'recomendations'

urlpatterns = [
    url(r'^$', views.recomendations, name='recomendations'),
]
