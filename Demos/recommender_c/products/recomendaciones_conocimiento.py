#!/usr/bin/env python
# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     recomendaciones_conocimiento.py
# Application:  products
# Componente:   Algoritmo de recomendación 
# Autor:    Samuel Vazquez
#
# Descripción:
# Este programa genera una lista de recomendaciones de productos 
# de acuerdo con perfil demográfico del usuario.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

# IMPORTANTE: importe el archivo de configuracion de los algoritmos
import recomendaciones_config

from django.db.models import Q
from .models import Product
from .models import Users



tipos_usuarios = {
'joven' : "extraer_edad(usuario.Nacimiento) < 21", 
'adulto' : "extraer_edad(usuario.Nacimiento) >= 21 and extraer_edad(usuario.Nacimiento) < 60",
'adulto_mayor' : "extraer_edad(usuario.Nacimiento) >= 60 and extraer_edad(usuario.Nacimiento) < 80",
'anciano' : "extraer_edad(usuario.Nacimiento) >= 80",

'casado_union_libre' : "usuario.Estado_civil == 'ul' or usuario.Estado_civil == 'c'",
'soltero' : "usuario.Estado_civil == 's'",
'todos': "True"
}

tipos_productos = {
'pediatras' : "Product.objects.filter(Q(Categoria='Pediatría') | Q(Categoria='Cirugía Pediátrica'))",
'med_familiar' : "Product.objects.filter(Q(Categoria='Medicina Familiar'))",
'ginecologos' : "Product.objects.filter(Categoria='Ginecología y Obstetricia')",
'geriatras' : "Product.objects.filter(Categoria='Geriatría')",
'cardiologos' : "Product.objects.filter(Q(Categoria='Cardiología') | Q(Categoria='Cirugía Cardiovascular y Torácica'))",
'angiologos' : "Product.objects.filter(Categoria='Angiología')",
'neumologos' : "Product.objects.filter(Categoria='Neumología')",
'otorrinos' : "Product.objects.filter(Categoria='Otorrinolaringología')",
}


def recomendacion_por_reglas(usuario):
	# recolecta los tipos de usuairos que son compatibles con el usuario actual
	tipos_usuario_actual = perfil_usuario(usuario)
	print "tipos usuario: ", tipos_usuario_actual 
	
	# clasifica al usuario activo en un perfil de usuario
	perfiles_activos_usuario_actual = perfiles_activos_usuario(tipos_usuario_actual)
	print "perfiles usuario: ", perfiles_activos_usuario_actual

	# genera la lista de pares (necesidad, num_prod) para cada necesidad en los
	# los perfiles compatibles del usuario actual
	necesidades_usuario_actual = necesidades_usuario(perfiles_activos_usuario_actual)
	print "necesidades_usuario_actual: ", necesidades_usuario_actual

	# genera la sintaxis de a consulta a la base de datos a traves del Django Framework
	consulta_productos_recomendados = consulta_productos_necesarios(usuario, necesidades_usuario_actual)
	
	metadatos_recomendacion = {'perfil':tipos_usuario_actual}
	print "total de productos recomendados: ", len(consulta_productos_recomendados)
	return consulta_productos_recomendados, metadatos_recomendacion


def consulta_productos_necesarios(usuario, necesidades_usuario_actual):
	filtrar_ciudad = False
	productos_recomendados_global = []
	for cada_necesidad in necesidades_usuario_actual:
		consulta = ''
		if cada_necesidad[0] in recomendaciones_config.necesidades_satisfechas:
			productos_reco_actual = []
			for cada_tipo_producto in recomendaciones_config.necesidades_satisfechas[cada_necesidad[0]]:
				if cada_tipo_producto in tipos_productos:
					consulta += tipos_productos[cada_tipo_producto] + " | "
			consulta = consulta[:len(consulta)-2]
			productos_recomendados = eval(consulta)
			if filtrar_ciudad:
				productos_recomendados = productos_recomendados.filter(Q(Estado=usuario.Ciudad) | Q(Municipio=usuario.Ciudad))
			productos_recomendados = productos_recomendados[:cada_necesidad[1]]
			productos_recomendados_global += productos_recomendados
	return productos_recomendados_global


def necesidades_usuario(perfiles_activos_usuario_actual):
	necesidades = []
	for cada_perfil in perfiles_activos_usuario_actual:
		num_max = recomendaciones_config.perfiles_usuarios[cada_perfil]['num_max_productos']
		for i in range(0, len(recomendaciones_config.perfiles_usuarios[cada_perfil]['necesidades'])):
			nec_actual = recomendaciones_config.perfiles_usuarios[cada_perfil]['necesidades'][i]
			num_actual = int(num_max * recomendaciones_config.perfiles_usuarios[cada_perfil]['ponderacion_lista'][i])
			print "necesidades ponderadas: ", nec_actual, num_actual

			necesidades.append((nec_actual, num_actual))

	return necesidades

def perfiles_activos_usuario(tipos_usuario_actual):
	perfiles_activos = []
	for cada_perfil in recomendaciones_config.perfiles_usuarios:
		pertenece = True
		for cada_atributo in recomendaciones_config.perfiles_usuarios[cada_perfil]['perfil']:
			pertenece = pertenece and cada_atributo in tipos_usuario_actual
		if pertenece:
			perfiles_activos += [cada_perfil]
	return perfiles_activos

def perfil_usuario(usuario):
	etiquetas_perfil = []
	for cada_tipo in tipos_usuarios:
		# evalua la condición de pertenencia
		if eval(tipos_usuarios[cada_tipo]):
			etiquetas_perfil.append(cada_tipo) #append if true
	return etiquetas_perfil

def extraer_edad(Nacimiento):
	nacimiento =  Nacimiento.split('/')
	valids_user_bd = []
	if len(nacimiento) == 3:
		return 100 + 16 - int(unicode(nacimiento[2]).encode('utf8'))
	else:
		return 0
	




