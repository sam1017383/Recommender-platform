# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     views.py
# Application:  data
# Componente:   vistas 
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# Este programa contiene las vistas de la aplicación data que
# se encarga de cargar información a la tabla auth_user y a la 
# tablas product_extras.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

from django.shortcuts import render, get_object_or_404 
from django.http import Http404, HttpResponse
from django.template import Context, loader
from django.contrib.auth.models import User
from data.models import *
import datetime

# Create your views here.

# **************************************************************
# Vista:     Index
#
# Descripción:
# Esta vista se encarga de cargar los usuarios de la tabla Users
# hacia la tabla auth_user del framework Django para permitir la 
# autenticación y autorización de ingreso al sistema.
# Se genera de manera automática el Password del usuario
# Por último permite la carga de la tabla de Product_extras con 
# los datos por default
# 
# Parámetros:
# @request 
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
def index(request):
    #Inicio de carga de todos los usuarios de la tabla Users a auth_user
    users_list = Users.objects.all()
    estatus = "Sin iniciar"
    for usuario in users_list:

        # Se inicializan las variables necesarias para inicio de sesión 
        username = "micorreonuevo@localhost.com"
        password = "Password_"+str(usuario.id)
            
        if len(usuario.Contacto) > 1:
            email=usuario.Contacto
            username = usuario.Contacto

            first_name = usuario.Nombre
            last_name = usuario.Apellido_p
        
            # Se escriben los registros en la Tabla auth_user de acuerdo con 
            # los datos de la tabla Users y la generación del Password de la 
            # linea 25
            try:
                actualUser = User.objects.get(username=username)
            except User.DoesNotExist:    
                actualUser = User.objects.create_user(username, email, password, id=usuario.id)
                actualUser.first_name = first_name
                actualUser.last_name = last_name
                actualUser.save()
            #FIN de carga de todos los usuarios de la tabla Users a auth_user
        



        

    #Inicio de carga de predeterminada de valores en la tabla product_extras
    product_list = Product.objects.all()
    for producto in product_list:
        try:
            productoExtra = Product_extras.objects.get(Product=producto)
        except Product_extras.DoesNotExist:    
            productoExtra = Product_extras(Product=producto, Imagen_fuente='images/default.png', 
                Calificacion_promedio=0.0, Precio=0.00, Descuento=0.00)
            productoExtra.save()
    #FIN de carga de predeterminada de valores en la tabla product_extras
    
    estatus = "Terminado"

    template = loader.get_template('data/index.html')
    context = {
        'estatus': estatus
    }
    return HttpResponse(template.render(context, request))