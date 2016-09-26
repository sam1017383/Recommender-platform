#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from products.models import Product
from products.models import Users
from products.models import Calificaciones
from products.models import Product_extras

import re
import datetime

busqueda_esquema = {
'nombre' : "Q(Nombre__icontains = 'ABCDEFG' )",
'categoria' : "Q(Categoria__icontains = 'ABCDEFG' )",
'estado' : "Q(Estado__icontains = 'ABCDEFG' )",
'municipio' : "Q(Municipio__icontains = 'ABCDEFG' )",
'colonia' : "Q(Colonia__icontains = 'ABCDEFG' )",
}



def coincidencia(texto_entrada):
	#print "texto entrada ::", texto_entrada
	if texto_entrada != "":
		
		sentencia = "" 
		terminos_busqueda = texto_entrada.split(' ')
		for cada_termino in terminos_busqueda:
			consulta = "" 
			for cada_restriccion in busqueda_esquema:
				consulta += busqueda_esquema[cada_restriccion] + " | "
			consulta = re.sub("ABCDEFG", cada_termino, consulta)
			consulta = consulta[:len(consulta)-2]
			sentencia += "Product.objects.filter("+consulta+") & "
		
		productos_encontrados = eval(sentencia[:len(sentencia)-2])
			
		return productos_encontrados
	
	else:
		return []

def productos_comentados_ciudad(ciudad):
	productos_base = Product.objects.filter(Q(Estado__icontains=ciudad)|Q(Municipio__icontains=ciudad)).values_list('id', flat=True)
	#print productos_base
	calificaciones_positivas = Calificaciones.objects.filter(Q(calificacion_producto__gte=3)).values_list('product_id', flat=True)
	#print calificaciones_positivas
	productos_mejor_comentados = []

	for cada_producto in productos_base:
		if cada_producto in calificaciones_positivas:
			productos_mejor_comentados.append(Product.objects.get(pk=cada_producto))

	return productos_mejor_comentados



def productos_nuevos(prod_max, dias):
	fecha_comparacion = datetime.date.today() - datetime.timedelta(days=dias)

	productos_base = Product_extras.objects.filter(Q(Fecha_alta__gt=fecha_comparacion)).values_list('Product_id', flat=True)

	productos_base = productos_base
	productos_nuevos = []
	i = 0
	for cada_producto in productos_base:
		productos_nuevos.append(Product.objects.get(pk=cada_producto))
		i += 1
		if i>prod_max:
			return productos_nuevos

	return productos_nuevos

	







