#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from .models import Product
from .models import Users

import re


busqueda_esquema = {
'nombre' : "Product.objects.filter(Nombre__icontains = 'ABCDEFG' )",
'categoria' : "Product.objects.filter(Categoria__icontains = 'ABCDEFG' )",
'estado' : "Product.objects.filter(Estado__icontains = 'ABCDEFG' )",
'municipio' : "Product.objects.filter(Municipio__icontains = 'ABCDEFG' )",
'colonia' : "Product.objects.filter(Colonia__icontains = 'ABCDEFG' )",

}



def coincidencia(texto_entrada):

	print "texto entrada ::", texto_entrada
	
	if texto_entrada != "":
		consulta = ""
		for cada_restriccion in busqueda_esquema:
			consulta += busqueda_esquema[cada_restriccion] + " | "
		consulta = re.sub("ABCDEFG", texto_entrada, consulta)
		#print "consulta de busqueda ::", consulta[:len(consulta)-2]
		productos_buscados = eval(consulta[:len(consulta)-2])
		return productos_buscados
	else:
		return False






