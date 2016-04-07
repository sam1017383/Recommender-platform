# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     urls.py
# Application:  products
# Componente:   url
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# Este programa identifica el patrón de la dirección solicitada 
# para asociarla con la vista correspondiente y parámetros 
# enviados por la misma url.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

from django.conf.urls import patterns, url
from products import views

#write urls aptterns of pruebax-views
urlpatterns = [
	# Envia a vista index con URL products/
	url(r'^$', views.index, name='index'),
	# Envia a vista detail con URL products/{#product_id}/
    url(r'^(?P<product_id>\d+)/$', views.detail, name='detail'),
    url(r'^busqueda/$', views.index_busqueda, name='index_busqueda'),
]