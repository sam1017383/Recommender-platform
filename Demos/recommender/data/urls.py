from django.conf.urls import patterns, url

#Patterns
from data import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]