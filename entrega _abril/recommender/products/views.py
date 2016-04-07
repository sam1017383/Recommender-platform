#!/usr/bin/env python
# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     views.py
# Application:  products
# Componente:   vistas 
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# Este programa contiene las vistas de la aplicación products que
# se encarga de cargar información de las recomendaciones de 
# productos, así como el detalle del producto seleccionado.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

# Declaración de librerias
from django.shortcuts import render, get_object_or_404 
from django.conf.urls.static import static
from django.http import Http404, HttpResponse
from django.template import Context, loader
from products.models import *
from django.contrib.auth.decorators import login_required

import recomendaciones_conocimiento
import recomendaciones_contenido
import recomendaciones_filtrado_colaborativo
import busqueda
import datetime, random
import re

# Create your views here.

# **************************************************************
# Vista:     Index
#
# Descripción:
# Vista que genera las listas de los diferentes carruseles de 
# recomendaciones y realiza el calculo promedio de las califica-
# ciones por producto, enviandolos datos al template 
# /products/index.html
# 
# Parámetros:
# @request 
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
def recomendaciones_xti(usuario):
    #Se generan las lista que se van a presentar en el index
    
    nombre_usuario = str(usuario.Nombre).lower().capitalize() +  " " + str(usuario.Apellido_p).lower().capitalize()
    ciudad_usuario = str(usuario.Ciudad).lower().capitalize()
    contacto_usuario = str(usuario.Contacto).lower()
    listas_productos = []

     # Carrusel de productos que te han gustado
    productos_calificados = recomendaciones_contenido.productos_calificados(usuario)
    if len(productos_calificados) > 0:
        listas_productos.append({'titulo': 'Productos que has calificado', 'productos': productos_calificados})
    else:
        print "No hay productos en Productos que has calificado"


    # Recomendaciones lo mas comentado en tu ciudad
    productos_comentados_ciudad = busqueda.productos_comentados_ciudad(15, ciudad_usuario)
    if len(productos_comentados_ciudad) > 0:
        listas_productos.append({'titulo': 'Lo más comentado en tu ciudad', 'productos': productos_comentados_ciudad})
    else:
        print "No hay productos en Lo más comentado en tu ciudad"

    # Recomendaciones por perfil
    productos_perfil = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    if len(productos_perfil) > 0:
        listas_productos.append({'titulo': 'Recomendaciones a tu pefil', 'productos': productos_perfil})
    else:
        print "No hay productos en Recomendaciones a tu pefil"

    # Alianzas nuevas en tu ciudad
    productos_nuevos = busqueda.productos_nuevos(15, 90)
    if len(productos_nuevos) > 0:
        listas_productos.append({'titulo': 'Nuevas alianzas X-ti', 'productos': productos_nuevos})
    else:
        print "No hay productos en Nuevas alianzas X-ti"
    


    # Recomendaciones usuarios socialmente similares
    productos_usuarios_similares = recomendaciones_contenido.recomendaciones_usuarios_similares(usuario, 15)
    if len(productos_usuarios_similares) > 0:
        listas_productos.append({'titulo': 'Usuarios como tú recomiendan', 'productos': productos_usuarios_similares})
    else:
        print "No hay productos en Usuarios como tú recomiendan"


    # Carrusel de productos similares
    productos_similares = recomendaciones_contenido.recomendacion_similares(usuario)
    if len(productos_similares) > 0:
        listas_productos.append({'titulo': 'Productos similares a los que te han gustado', 'productos': productos_similares})
    else:
        print "No hay productos en Productos similares a los que te han gustado"

    
    # Recomendaciones productos_fc
    productos_fc = recomendaciones_filtrado_colaborativo.recomendaciones_fc(usuario)
    if len(productos_fc) > 0:
        listas_productos.append({'titulo': 'Usuarios con gustos similares les han gustado', 'productos': productos_fc})
    else:
        print "No hay productos en Usuarios con gustos similares les han gustado"

    # Recomendaciones hibridas
    recomendaciones_predictivas = recomendaciones_filtrado_colaborativo.recomendaciones_hibridas(productos_fc)
    if len(recomendaciones_predictivas) > 0:
        listas_productos.append({'titulo': 'Productos interesantes para tí', 'productos': recomendaciones_predictivas})
    else:
        print "No hay productos en Productos interesantes para tí"

    return listas_productos






@login_required(login_url='/access/login.html')
def index(request):
    #Se generan las lista que se van a generar en el index
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    nombre_usuario = str(usuario.Nombre).lower().capitalize() +  " " + str(usuario.Apellido_p).lower().capitalize()
    ciudad_usuario = str(usuario.Ciudad).lower().capitalize()
    contacto_usuario = str(usuario.Contacto).lower()
    print "contacto_usuario: ", contacto_usuario
    print "id_usuario: ", str(usuario_activo.id)


    
    
    if 'recomendaciones_sesion' not in request.session.keys():
        print "HOME prev--------> ", str(request.session.keys())
        reco_listas = recomendaciones_xti(usuario)
        request.session['recomendaciones_sesion'] = reco_listas
        print "HOME post--------> ", str(request.session.keys())
    else:
        reco_listas = request.session.get('recomendaciones_sesion', None)



    template = loader.get_template('products/index.html')

    context = {
        'nombre_usuario': nombre_usuario,
        'ciudad_usuario': ciudad_usuario,
        'contacto_usuario': contacto_usuario,
        'recomendaciones': reco_listas
    }
    

    return HttpResponse(template.render(context, request))




# **************************************************************
# Vista:     Index
#
# Descripción:
# Vista que genera las listas de los diferentes carruseles de 
# recomendaciones y realiza el calculo promedio de las califica-
# ciones por producto, enviandolos datos al template 
# /products/index.html
# 
# Parámetros:
# @request 
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
@login_required(login_url='/access/login.html')
def index_busqueda(request):
    #Se generan las lista que se van a generar en el index
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    nombre_usuario = str(usuario.Nombre).lower().capitalize() +  " " + str(usuario.Apellido_p).lower().capitalize()
    ciudad_usuario = str(usuario.Ciudad).lower().capitalize()
    contacto_usuario = str(usuario.Contacto).lower()

    

    
    # Carrusel de resultados de busqueda
    productos_busqueda = []
    reco_listas =[]
    

    if 'recomendaciones_sesion' not in request.session.keys():
        reco_listas = recomendaciones_xti(usuario)
        request.session['recomendaciones_sesion'] = reco_listas
    else:
        reco_listas = request.session.get('recomendaciones_sesion', None)

    if request.GET.get('busqueda_main') is not None: 
        texto_busqueda = request.GET.get('busqueda_main')
        productos_busqueda = busqueda.coincidencia(texto_busqueda)

    if len(productos_busqueda) > 0:
        reco_listas.insert(0,{'titulo': 'Resultados de búsqueda para: ' + str(texto_busqueda), 'productos': productos_busqueda})
    else:
        print "No hay productos en Resultados de búsqueda"

    template = loader.get_template('products/index.html')
    
    context = {
        'nombre_usuario': nombre_usuario,
        'ciudad_usuario': ciudad_usuario,
        'contacto_usuario': contacto_usuario,
        'recomendaciones': reco_listas
    }
    

    return HttpResponse(template.render(context, request))



# **************************************************************
# Vista:     Detail
#
# Descripción:
# Vista que muestra el producto o elemento seleccionado en el  
# carrusel de recomendaciones, enviando los datos del producto  
# al template /products/detail.html
# 
# Parámetros:
# @request 
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
@login_required(login_url='/access/login.html')
def detail(request, product_id):

    #Buscar Lista de Productos recomendados para el usuario
    valorCalificacion = 0
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    nombre_usuario = str(usuario.Nombre).lower().capitalize() +  " " + str(usuario.Apellido_p).lower().capitalize()
    ciudad_usuario = str(usuario.Ciudad).lower().capitalize()
    contacto_usuario = str(usuario.Contacto).lower()
    productos_similares = recomendaciones_contenido.k_vecinos_productos(product_id, 6)
    #Busca el producto seleccionado
    Producto = get_object_or_404(Product, pk=product_id)

    #Busca objeto de Producto con calificacion para el usuario
    try:
        calificacionExistente = Calificaciones.objects.get(product=Producto, users=usuario)
    except Calificaciones.DoesNotExist:
        comentario = ""
        valorCalificacion = 0
        calificacionExistente = Calificaciones(product=Producto, users=usuario, calificacion_producto=valorCalificacion, comentario=comentario)

    if request.POST.get('comentario') is not None:
        comentario = request.POST.get('comentario')
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
    else:
        if calificacionExistente.comentario is not None:
            comentario = calificacionExistente.comentario
        else:
            comentario = ""

    if request.POST.get('calificacion') is not None:
        valorCalificacion = request.POST.get('calificacion')
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
        productoExtra = Product_extras()
        productoExtra = productoExtra.calculaPromedio(Producto)
        
        if 'recomendaciones_sesion' in request.session.keys():
            reco_listas = recomendaciones_xti(usuario)
            request.session['recomendaciones_sesion'] = reco_listas


    else:
        if calificacionExistente.calificacion_producto is not None:
            valorCalificacion = calificacionExistente.calificacion_producto
        else:
            valorCalificacion = 0

    #Busca comentarios del mismo Producto por otros usuarios
    try:
        comentariosExistentes = Calificaciones.objects.filter(product=Producto).order_by('-fecha').select_related('users')[:20]
    except Calificaciones.DoesNotExist:
        comentariosExistentes = None

    #Construccion del template y envio de Respuesta
    template = loader.get_template('products/detail.html')
    context = {
        'latest_productos_list': productos_similares,
        'Producto': Producto,
        'id_user': usuario_activo.id,
        'calificacionExistente': calificacionExistente,
        'comentario': comentario,
        'valorCalificacion': valorCalificacion,
        'comentariosExistentes': comentariosExistentes,
        'nombre_usuario': nombre_usuario,
        'ciudad_usuario': ciudad_usuario,
        'contacto_usuario': contacto_usuario,
    }

    return HttpResponse(template.render(context, request))