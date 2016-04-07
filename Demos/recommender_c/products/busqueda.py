#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from .models import Product
from .models import Users

import re


busqueda_esquema = {
'nombre' : "Q(Nombre__icontains = 'ABCDEFG' )",
'categoria' : "Q(Categoria__icontains = 'ABCDEFG' )",
'estado' : "Q(Estado__icontains = 'ABCDEFG' )",
'municipio' : "Q(Municipio__icontains = 'ABCDEFG' )",
'colonia' : "Q(Colonia__icontains = 'ABCDEFG' )",

}



def coincidencia(texto_entrada):

	
	
	print "texto entrada ::", texto_entrada
	
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








