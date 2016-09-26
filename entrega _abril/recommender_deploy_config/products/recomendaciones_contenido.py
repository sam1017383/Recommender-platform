#!/usr/bin/env python
# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     recomendaciones_contenido.py
# Application:  products
# Componente:   Algoritmo de recomendación 
# Autor:    Samuel Vazquez
#
# Descripción:
# Este programa genera una lista de recomendaciones de productos 
# de acuerdo con las compras históricas
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

# IMPORTANTE: importe el archivo de configuracion de los algoritmos
import recomendaciones_config
limite_k = recomendaciones_config.rec_contenido_k_vecinos
limite_lista = recomendaciones_config.rec_contenido_max
metodo_similitud = recomendaciones_config.rec_contenido_similitud

from django.db.models import Q
from .models import Product
from .models import Users
from .models import Calificaciones

from django.db.models.query import EmptyQuerySet

import re



def productos_calificados(usuario):
    calificaciones_usuario_activo = Calificaciones.objects.filter(users=usuario.id).order_by('calificacion_producto').values_list('product_id', flat=True)
    productos_calif = Product.objects.filter(pk__in=list(calificaciones_usuario_activo))
    return productos_calif



def productos_calificados_rec(usuario, longitud):
    calificaciones_usuario_activo = Calificaciones.objects.filter(users=usuario.id).order_by('calificacion_producto').values_list('product_id', flat=True)
    productos_calif = Product.objects.filter(pk__in=list(calificaciones_usuario_activo))
    return productos_calif[:longitud]


def recomendacion_similares(usuario, longitud):
    # juntar los productos calificados
    productos_similares = []
    productos_base_calif = Calificaciones.objects.filter(users=usuario.id).order_by('calificacion_producto').values_list('product_id', flat=True)
    productos_base = Product.objects.filter(pk__in=list(productos_base_calif))
    # agregar k vecinos de cada producto calificado
    for cada_producto_base in productos_base:
        #print "producto base: ", cada_producto_base.Nombre
        vecinos = k_vecinos_productos(cada_producto_base.id, limite_k)
        productos_similares += vecinos

    return productos_similares[:longitud]

def k_vecinos_productos(product_id, k):
    
    producto = Product.objects.get(pk=product_id)
    producto_latitud = producto.Latitud
    producto_longitud = producto.Longitud
    producto_categoria = producto.Categoria
    mce_count = 0
    mcc_count = 0

    #0.01	0° 00′ 36″	town or village	1.1132 km
    # Calculado para buscar cada 1.1132 km a la redonda
    paso = 0.01
    numero_circulos = 4

    productos_circulo_actual = Product.objects.get(pk=product_id)
    productos_circulo_actual_cat = Product.objects.get(pk=product_id)
    mejor_consulta_exacta = Product.objects.get(pk=product_id)
    mejor_consulta_cercana = Product.objects.get(pk=product_id)

    #itera en circulos de cercania
    
    for circulo_actual in range(1,numero_circulos):
    	intervalo_latitud_min = float(producto_latitud) - paso * circulo_actual
    	intervalo_latitud_max = float(producto_latitud) + paso * circulo_actual
    	intervalo_longitud_min = float(producto_longitud) - paso * circulo_actual
    	intervalo_longitud_max = float(producto_longitud) + paso * circulo_actual

    	productos_circulo_actual = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min)).exclude(pk=product_id) 
    	productos_circulo_actual_cat = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min) & Q(Categoria=producto_categoria)).exclude(pk=product_id) 
    	
    	if productos_circulo_actual_cat.count() > k:	
    		return list(productos_circulo_actual_cat)[:k]

    	if 0 < productos_circulo_actual_cat.count() < k:
    		mejor_consulta_exacta = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min) & Q(Categoria=producto_categoria)).exclude(pk=product_id) 
    		mce_count = mejor_consulta_exacta.count()
    	if 0 < productos_circulo_actual.count():
    		mejor_consulta_cercana = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min)).exclude(pk=product_id)
    		mcc_count = mejor_consulta_cercana.count()

    if mce_count > 0:
    	return list(mejor_consulta_exacta) + list(mejor_consulta_cercana[0:k-mce_count])
    elif mcc_count > 0:
    	return list(mejor_consulta_cercana)[:k]
    else:
    	return []


def k_vecinos_lista_productos(product_list, k):

    if len(product_list) > 0:

    	k_prod = int(k / len(product_list))
    	productos_similares_lista = []
    	for cada_producto in product_list:
    		productos_similares_lista += k_vecinos_productos(cada_producto.id, k_prod)
    	return productos_similares_lista
    else:
    	return []

    





def usuarios_similares(usuario_x, usuario_y):
	if abs(extraer_edad(usuario_x.Nacimiento) - extraer_edad(usuario_x.Nacimiento)) < 10 and usuario_x.Estado_civil == usuario_y.Estado_civil and usuario_x.Hijos == usuario_y.Hijos:
		return True
	else:
		return False

def extraer_edad(Nacimiento):
    nacimiento =  Nacimiento.split('/')
    valids_user_bd = []
    if len(nacimiento) == 3:
        return 100 + 16 - int(unicode(nacimiento[2]).encode('utf8'))
    else:
        return 0
        

def recomendaciones_usuarios_similares(usuario, prod_max):
    recomendaciones_usuarios_similares = []
    i = 0
    calificaciones_positivas = Calificaciones.objects.filter(Q(calificacion_producto__gte=3))
    for cada_calificacion_positiva in calificaciones_positivas:
        if usuarios_similares(usuario, Users.objects.get(pk=cada_calificacion_positiva.users.id)):
            recomendaciones_usuarios_similares.append(Product.objects.get(pk=cada_calificacion_positiva.product.id))
            i += 1
        if i > prod_max:
            return recomendaciones_usuarios_similares
    return recomendaciones_usuarios_similares





        
