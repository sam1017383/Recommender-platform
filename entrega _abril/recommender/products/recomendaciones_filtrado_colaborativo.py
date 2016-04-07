#!/usr/bin/env python
# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     recomendaciones_filtrado_colaborativo.py
# Application:  products
# Componente:   Algoritmo de recomendación 
# Autor:    Samuel Vazquez
#
# Descripción:
# Este programa genera una lista de recomendaciones de productos 
# de acuerdo con las compras históricas de todos los usuarios
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

# IMPORTANTE: importe el archivo de configuracion de los algoritmos
import recomendaciones_config
limite_lista = recomendaciones_config.rec_filtrado_colaborativo_max
limite_lista_h = recomendaciones_config.rec_hibrido_max
metodo_similitud = recomendaciones_config.rec_filtrado_colaborativo_similitud

from django.db.models import Q
from products.models import Product
from products.models import Users
from products.models import Calificaciones

from django.db.models.query import EmptyQuerySet
from django.db.models import Avg


import re
import random
import math





def recomendaciones_fc(usuario):

    # encuentra los productos base
    calificaciones = Calificaciones.objects.filter(users=usuario.id)
    # encuentra los usuarios con coincidencias
    calificaciones_coincidencia = []
    calificaciones_coincidencia_completo = []
    usados = []
    usuarios_productos = {}
    for cada_calificacion in calificaciones:

        calificaciones_coincidencia = Calificaciones.objects.filter(product=cada_calificacion.product_id)
        for cada_calificacion in calificaciones_coincidencia:
            if str(cada_calificacion.users_id) not in usados:
                usados.append(str(cada_calificacion.users_id))
                usuarios_productos[str(cada_calificacion.users_id)] = [cada_calificacion.product_id]
            else:
                usuarios_productos[str(cada_calificacion.users_id)] += [cada_calificacion.product_id]
    #print "coincidencias: ", usuarios_productos
    usuarios_similares_fc = []
    for cada_usuario_similar in usuarios_productos.keys():
        # usuarios que solo han evaluado un producto en comun
        calif_usuario_u_prom = Calificaciones.objects.filter(users=usuario.id).aggregate(Avg('calificacion_producto'))
        calif_usuario_v_prom = Calificaciones.objects.filter(users=cada_usuario_similar).aggregate(Avg('calificacion_producto'))
        prom_u = calif_usuario_u_prom['calificacion_producto__avg']
        prom_v = calif_usuario_v_prom['calificacion_producto__avg']

        similitud = similitud_pearson(usuario.id, cada_usuario_similar, usuarios_productos[cada_usuario_similar], prom_u, prom_v)
        #print "HIER: similitud: ", similitud, "con usuario: ", cada_usuario_similar, "usuario actual: ", usuario.id
        usuarios_similares_fc.append((cada_usuario_similar, similitud))

    usuarios_similares_fc.sort(key=lambda tup: tup[1], reverse=True)
    #print usuarios_similares_fc
    prod_rec_fc = []
    for cada_usuario_fc_ordenado in usuarios_similares_fc:
        if cada_usuario_fc_ordenado[1] > 0.5:
            calif_rec_fc = Calificaciones.objects.filter(Q(users_id=cada_usuario_fc_ordenado[0]) & Q(calificacion_producto__gt=4)).values_list('product_id', flat=True)
            prod_rec_fc += Product.objects.filter(pk__in=list(calif_rec_fc))
    
    return prod_rec_fc[:limite_lista]

def similitud_pearson(id_activo, id_usuario_x, lista_produtos, prom_u, prom_v):
    # sim = ( sum (cu - prom_u) * (cv - prom_v) ) / sqrt( sum (cu - prom_u)^2 )  * sqrt( sum (cv - prom_v)^2 )
    suma_numerador = 0.0
    suma_denominador_u = 0.0
    suma_denominador_v = 0.0

    for cada_producto in lista_produtos:
        print "cada_producto: ", cada_producto
        u_i = Calificaciones.objects.filter(Q(users_id=id_activo) & Q(product_id=cada_producto))[0]
        u_i = u_i.calificacion_producto
        v_i = Calificaciones.objects.filter(Q(users_id=id_usuario_x) & Q(product_id=cada_producto))[0]
        v_i = v_i.calificacion_producto

        suma_numerador += (u_i - prom_u) * (v_i - prom_v)
        suma_denominador_u += (u_i - prom_u) * (u_i - prom_u)
        suma_denominador_v += (v_i - prom_v) * (v_i - prom_v)

    if suma_numerador == 0 or suma_denominador_u == 0 or suma_denominador_v == 0:
        similitud = 0
    else:
        similitud = suma_numerador / (math.sqrt(suma_denominador_u) * math.sqrt(suma_denominador_v))
    return similitud


def recomendaciones_hibridas(recomendaciones_fc):
    reco_hibridas = []

    for cada_producto_fc in recomendaciones_fc:
        reco_hibridas += k_vecinos_productos(cada_producto_fc.id,1)
    return reco_hibridas[:limite_lista_h]


def k_vecinos_productos(product_id, k):
    
    producto = Product.objects.get(pk=product_id)
    producto_latitud = producto.Latitud
    producto_longitud = producto.Longitud
    producto_categoria = producto.Categoria
    mce_count = 0
    mcc_count = 0

    #0.01   0° 00′ 36″  town or village 1.1132 km
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




        	

