from django.conf.urls import url

from . import views

app_name = 'contact'

urlpatterns = [
    url(r'^$', views.contact, name='contact'),
    url(r'^message_success/$', views.success, name='success'),
    url(r'^message_failure/$', views.failure, name='failure'),
]
