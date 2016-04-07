# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     urls.py
# Application:  recommender
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

"""recommender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#   url(r'^data/', include('data.urls')),
    url(r'^access/', include('access.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^', include('access.urls')),
]
