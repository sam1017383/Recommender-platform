from django.conf.urls import patterns, url
#from django.contrib import admin

from products import views

#write urls aptterns of pruebax-views
urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^detalle/(?P<product_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<product_id>\d+)/$', views.detail, name='detail'),
]