# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     wsgi.py
# Application:  recommender
# Autor:    Framework
# Empresa:  Infotec
#
# Descripción:
# N/A.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

"""
WSGI config for recommender project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

application = get_wsgi_application()
