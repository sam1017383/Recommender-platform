# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     urls.py
# Application:  access
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


from django.conf.urls import url
from . import views

app_name = 'access'

#Describe the urls patterns
urlpatterns = [
	# Envia a vista index con URL access/
    url(r'^$', views.index, name='index'),
    # Envia a vista login_view con URL access/login
    url(r'^login', views.login_view, name='login'),
    # Envia a vista logout_view con URL access/logout
    url(r'^logout', views.logout_view, name='logout'),
]