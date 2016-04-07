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



comentarios_predefinidos = [
    "esto es nulo",
    "Este producto es pésimo",
    "El producto es muy deficiente, no recomendable",
    "El lugar no es bueno, mejor evítalo",
    "Buen servicio! recomendable!",
    "Excelente! Magnífico!"
    
]



@login_required(login_url='/access/login.html')
def index(request):
    #Se generan las lista que se van a generar en el index
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    nombre_usuario = usuario.Nombre +  " " + usuario.Apellido_p


    ## populate comments
    # se insertan 10,000 comentarios de 1000 usuarios sobre 1000 productos, 10 por usuario
    # se colectan 1000 usuarios al azar
    #todos_usuarios = Users.objects.order_by('?')[:1000]
    #todos_productos = Product.objects.order_by('?')[:1000]
    #calificaciones_por_usuario = 10
    #for cada_usuario in todos_usuarios:
    #    print "HEY: Ho ", cada_usuario.Nombre
    #    for i in range(0, calificaciones_por_usuario):
    #        valorCalificacion = random.randint(1, 5)
    #        producto_calificar = todos_productos[random.randint(0, len(todos_productos)-1)]
    #        comentario = comentarios_predefinidos[valorCalificacion]
    #        calificacionExistente = Calificaciones(product=producto_calificar, users=cada_usuario, calificacion_producto=valorCalificacion, comentario=comentario)
    #        print "cali: ", calificacionExistente
    #        calificacionExistente.save()
    #valorCalificacion = request.POST.get('calificacion')
    #calificacionExistente.calificacion_producto=valorCalificacion
    #calificacionExistente.comentario=comentario
    #calificacionExistente.save()



    # Carrusel de resultados de busqueda
    texto_busqueda = ""
    if request.GET.get('busqueda_main') is not None: 
        texto_busqueda = request.GET.get('busqueda_main')
    productos_busqueda = busqueda.coincidencia(texto_busqueda)
    productoExtra = Product_extras()
    for cada_producto in productos_busqueda:
        productoExtra = productoExtra.calculaPromedio(cada_producto)


    # Carrusel de productos que te han gustado
    productos_calificados = recomendaciones_contenido.productos_calificados(usuario)
    for productoEvaluado in productos_calificados:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Carrusel de productos similares
    productos_similares = recomendaciones_contenido.recomendacion_similares(usuario)
    for productoEvaluado in productos_similares:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones por perfil
    productos_perfil, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    for productoEvaluado in productos_perfil:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones productos_fc
    productos_fc = recomendaciones_filtrado_colaborativo.recomendaciones_fc(usuario)
    for productoEvaluado in productos_fc:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones hibridas
    recomendaciones_predictivas = recomendaciones_filtrado_colaborativo.recomendaciones_hibridas(productos_fc)
    for productoEvaluado in recomendaciones_predictivas:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)


    template = loader.get_template('products/index.html')
    perfil_usuario = recomendaciones_conocimiento.perfil_usuario(usuario)


    context = {
        'nombre_usuario_saludo': nombre_usuario,
        'perfil': perfil_usuario,
        'productos_busqueda': productos_busqueda,
        'productos_calificados': productos_calificados,
        'productos_similares': productos_similares,
        'productos_perfil': productos_perfil,
        'productos_predictivos': recomendaciones_predictivas,
        'productos_fc': productos_fc
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
    nombre_usuario = usuario.Nombre +  " " + usuario.Apellido_p
    

    
    # Carrusel de resultados de busqueda
    texto_busqueda = ""
    if request.GET.get('busqueda_main') is not None: 
        texto_busqueda = request.GET.get('busqueda_main')
    productos_busqueda = busqueda.coincidencia(texto_busqueda)
    productoExtra = Product_extras()
    for cada_producto in productos_busqueda:
        productoExtra = productoExtra.calculaPromedio(cada_producto)


    # Carrusel de productos que te han gustado
    productos_calificados = recomendaciones_contenido.productos_calificados(usuario)
    for productoEvaluado in productos_calificados:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Carrusel de productos similares
    productos_similares = recomendaciones_contenido.recomendacion_similares(usuario)
    for productoEvaluado in productos_similares:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones por perfil
    productos_perfil, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    for productoEvaluado in productos_perfil:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones productos_fc
    productos_fc = recomendaciones_filtrado_colaborativo.recomendaciones_fc(usuario)
    for productoEvaluado in productos_fc:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)

    # Recomendaciones hibridas
    recomendaciones_predictivas = recomendaciones_filtrado_colaborativo.recomendaciones_hibridas(productos_fc)
    for productoEvaluado in recomendaciones_predictivas:
        productoExtra = productoExtra.calculaPromedio(productoEvaluado)


    template = loader.get_template('products/index.html')
    perfil_usuario = recomendaciones_conocimiento.perfil_usuario(usuario)


    context = {
        'nombre_usuario_saludo': nombre_usuario,
        'perfil': perfil_usuario,
        'productos_busqueda': productos_busqueda,
        'productos_calificados': productos_calificados,
        'productos_similares': productos_similares,
        'productos_perfil': productos_perfil,
        'productos_predictivos': recomendaciones_predictivas,
        'productos_fc': productos_fc
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
    latest_productos_list, metadatos_recomendacion = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    latest_productos_list = recomendaciones_contenido.k_vecinos_productos(product_id, 10)
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
        'latest_productos_list': latest_productos_list[:100],
        'metadatos_usuario': metadatos_recomendacion,
        'Producto': Producto,
        'id_user': usuario_activo.id,
        'calificacionExistente': calificacionExistente,
        'comentario': comentario,
        'valorCalificacion': valorCalificacion,
        'comentariosExistentes': comentariosExistentes
    }

    return HttpResponse(template.render(context, request))