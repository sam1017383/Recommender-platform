from django.conf.urls import url

from . import views

app_name = 'access'

#Describe the urls patterns
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
]