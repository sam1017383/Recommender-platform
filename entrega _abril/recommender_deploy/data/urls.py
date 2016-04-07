# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     urls.py
# Application:  data
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

#Patterns
from data import views

urlpatterns = [
	# Envia a vista index con URL data/
    url(r'^$', views.index, name='index'),
]