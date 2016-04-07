# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     models.py
# Application:  data
# Componente:   Modelos
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# En este programa se declaran los modelos necesarios para el 
# funcionamiento correcto de la app data.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

from __future__ import unicode_literals
from django.db import models

# Se importa el modelo User del framework correspondiente a la 
# tabla auth_user la cual debe contener la información de 
# autenticación de usuarios
from django.contrib.auth.models import User

# Se importan los modelos de la app products 
from products.models import *

# Create your models here.


