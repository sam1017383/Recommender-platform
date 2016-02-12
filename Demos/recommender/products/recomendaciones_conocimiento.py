#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from .models import Product
from .models import Users

perfiles_usuarios = {
'familia_joven': {'perfil' : ['joven', 'con_hijos', 'casado_union_libre'],
                  'necesidades':['cuidar_ninos', 'cuidar_madre']},

'posible_abuelo': {'perfil' : ['adulto_mayor', 'con_hijos'],
                  'necesidades':['cuidar_ninos']},

'check_up_fumadores': {'perfil' : ['todos'],
                  'necesidades':['cuidar_corazon_circulacion', 'cuidar_pulmones_garganta']},

'check_up_tercera_edad': {'perfil' : [ 'anciano'],
                  'necesidades':['cuidar_vejez']},
}


necesidades_satisfechas = {
'cuidar_ninos':['pediatras', 'med_familiar'],
'cuidar_madre':['ginecologos'],
'cuidar_corazon_circulacion':['cardiologos', 'angiologos'],
'cuidar_pulmones_garganta':['otorrinos', 'neumologos'],
'cuidar_vejez':['geriatras'],
}


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
	perfil_usuario_actual = perfil_usuario(usuario)
	necesidades_usuario_actual = necesidades_usuario(perfil_usuario_actual)
	consulta_productos_recomendados = consulta_productos_necesarios(necesidades_usuario_actual)
	productos_recomendados = eval(consulta_productos_recomendados)
	metadatos_recomendacion = {'nombre_usuario': 'Samuel V', 'perfil':perfil_usuario_actual}
	return productos_recomendados, metadatos_recomendacion


def consulta_productos_necesarios(necesidades_usuario_actual):
	consulta = ''
	for cada_necesidad in necesidades_usuario_actual:
		if cada_necesidad in necesidades_satisfechas:
			for cada_tipo_producto in necesidades_satisfechas[cada_necesidad]:
				if cada_tipo_producto in tipos_productos:
					consulta += tipos_productos[cada_tipo_producto] + " | "
	return consulta[:len(consulta)-2]


def necesidades_usuario(perfil_usuario):
	necesidades = []
	for cada_perfil in perfiles_usuarios:
		pertenece = True
		for cada_atributo in perfiles_usuarios[cada_perfil]['perfil']:
			pertenece = pertenece and cada_atributo in perfil_usuario
		if pertenece:
			necesidades += perfiles_usuarios[cada_perfil]['necesidades']
	return necesidades

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
	




