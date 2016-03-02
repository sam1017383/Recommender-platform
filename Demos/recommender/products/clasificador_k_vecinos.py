#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from .models import Product
from .models import Users
from .models import Calificaciones

from django.db.models.query import EmptyQuerySet

import re


busqueda_esquema = {
'nombre' : "Product.objects.filter(Nombre__icontains = 'ABCDEFG' )",
'categoria' : "Product.objects.filter(Categoria__icontains = 'ABCDEFG' )",
'estado' : "Product.objects.filter(Estado__icontains = 'ABCDEFG' )",
'municipio' : "Product.objects.filter(Municipio__icontains = 'ABCDEFG' )",
'colonia' : "Product.objects.filter(Colonia__icontains = 'ABCDEFG' )",

}



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

    #itera en tres circulos de cercania
    
    for circulo_actual in range(1,numero_circulos):
    	intervalo_latitud_min = float(producto_latitud) - paso * circulo_actual
    	intervalo_latitud_max = float(producto_latitud) + paso * circulo_actual
    	intervalo_longitud_min = float(producto_longitud) - paso * circulo_actual
    	intervalo_longitud_max = float(producto_longitud) + paso * circulo_actual

    	productos_circulo_actual = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min)).exclude(pk=product_id) 
    	productos_circulo_actual_cat = Product.objects.filter(Q(Latitud__lte=intervalo_latitud_max) & Q(Latitud__gte=intervalo_latitud_min) & Q(Longitud__gte=intervalo_longitud_max) & Q(Longitud__lte=intervalo_latitud_min) & Q(Categoria=producto_categoria)).exclude(pk=product_id) 
    	
    	if productos_circulo_actual_cat.count() > k:
    		print "lol saliooo"    		
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
	if abs(extraer_edad(usuario_x.Nacimiento) - extraer_edad(usuario_x.Nacimiento)) < 5 and usuario_x.Estado_civil == usuario_y.Estado_civil and usuario_x.Hijos == usuario_y.Hijos and usuario_x.Ciudad == usuario_y.Ciudad:
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

def recomendaciones_usuarios_similares(usuario):
    recomendaciones_usuarios_similares = []
    calificaciones_positivas = Calificaciones.objects.filter(Q(calificacion_producto__gte=0))
    for cada_calificacion_positiva in calificaciones_positivas:
        if usuarios_similares(usuario, Users.objects.get(pk=cada_calificacion_positiva.users.id)):
            recomendaciones_usuarios_similares.append(Product.objects.get(pk=cada_calificacion_positiva.product.id))
    return recomendaciones_usuarios_similares


def recomendaciones_fc(usuario):
	# Recomendaciones productos_fc
    calificaciones = Calificaciones.objects.filter(users=usuario.id)

    productos_fc = []
    
    usuarios_fc = []

    usuarios_similares = []
    print "now in fc:: calificaciones length: ", len(calificaciones)
    for cada_producto_calificado in calificaciones:
        
        usuarios_similares += list(Calificaciones.objects.filter(Q(product=cada_producto_calificado.product.id)).exclude(users=usuario.id))
        print "now in fc:: usuarios que tambien calificaron length: ", len(usuarios_similares)
        for cada_usuario_similar in usuarios_similares:
            calificaciones_fc = Calificaciones.objects.filter(users=cada_usuario_similar.id).exclude(product=cada_producto_calificado.product.id).values_list('pk', flat=True)
            productos_fc += Product.objects.filter(pk__in=list(calificaciones_fc))
            print "now in fc:: productos  length: ", len(productos_fc)
    return productos_fc

        	


        




















