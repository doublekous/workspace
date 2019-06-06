from django.conf.urls import url

from medialibary import views

urlpatterns = [
    url(r'shishi/$', views.shishi, name='shishi'),
]