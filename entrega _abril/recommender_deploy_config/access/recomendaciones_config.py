#!/usr/bin/env python
# -*- coding: utf-8 -*-

# **************************************************************
# Archivo de configuración: recomendaciones_config.py
# Application:  recommender
# Autor:    Samuel Vazquez
#
# Descripción:
# Este archivo configura las recomendaciones que la aplicacion
# de recomendaciones en Django utiliza.
# Permite la reconfiguración paramétrica de las técnicas de
# recomendacion automática implementadas.
# 
# Fecha de creación: Febrero-2016
# Versión: 1.0 
# *************************************************************

# ***** IMPORTANTE: No modifique el nombre de las variables. 
#                   Modifique únicamente su contenido.

# *************************************************************
# Recomendaciones basadas en conocimiento del usuario:
#  - Genera recomendaciones si el usuario activo cumple con un
#    perfíl demográfico específico
#  - A cada perfil de usuario se le asocian necesidades
#  - Recolecta productos que satisfacen  necesidades específicas
#  
# Cada perfil de usuario se compone de la conjunción de varios
# tipos primitivos de usuario. 
# Los tipos predefinidos por defecto son:
# joven, adulto, adulto_mayor, anciano, casado_union_libre, 
# soltero y todos
#
# Cada necesidad puede satisfacerse por cualquiera de los 
# productos en un conjunto de categorias primitivas de productos.
# Las categorias predefinidas son: 
# pediatras, med_familiar, ginecologos, geriatras, cardiologos,
# angiologos, neumologos y otorrinos
#
#
# Para agregar un nuevo perfil de usuairo objetivo: 
#  1. Ingrese otro elemento al diccionario "perfiles_usuarios"
# 
# perfiles_usuarios = {
#
#   'nuevo_perfil': {'perfil' : [],
#                    'necesidades':[]},
#
#	...
# }
#  2. Describa en perfil en términos de una lista de cadenas con el
#     nombre de tipos primitivos de usuarios, antes mencionados
#     EJEMPLO:  'perfil' : ['joven', 'con_hijos', 'casado_union_libre']
#
#  3. Describa las necesidades en términos de una lista de cadenas con el
#     nombre de las ncesidades satisfechas enlistadas en el diccionario
#     "necesidades_satisfechas", definida por el usuario a continuación
#
#  4. Si desea espeficar una nueva necesidad satisfecha por un grupo
#     de productos, agrege una entrada al diccionario "necesidades_satisfechas":
# 
# necesidades_satisfechas = {
#
#   'nueva_necesidad_satisfecha':[]
#
#	...
# }
#
# 5. Describa los productos que satisfacen la necesidad en términos
#    de una lista de categorias primitivas de productos, antes mencionadas
#
#  ¡Eso es todo!
#  Si el usuario activo cumple con alguno o algunos de los perfiles,
#  Se generará una lista con los productos EN SU CIUDAD que cubran 
#  sus necesidades
# *************************************************************

perfiles_usuarios = {
'familia_joven': {'perfil' : ['joven', 'con_hijos', 'casado_union_libre'],
                  'necesidades':['cuidar_ninos', 'cuidar_madre'],
                  'ponderacion_lista':[0.5, 0.5],
                  'num_max_productos': 10},

'posible_abuelo': {'perfil' : ['adulto_mayor', 'con_hijos'],
                  'necesidades':['cuidar_ninos'],
                  'ponderacion_lista':[1],
                  'num_max_productos': 10},

'check_up_fumadores': {'perfil' : ['todos'],
                  'necesidades':['cuidar_corazon_circulacion', 'cuidar_pulmones_garganta'],
                  'ponderacion_lista':[0.8, 0.2],
                  'num_max_productos': 10},

'check_up_tercera_edad': {'perfil' : [ 'anciano'],
                  'necesidades':['cuidar_vejez'],
                  'ponderacion_lista':[1],
                  'num_max_productos': 10},
}


necesidades_satisfechas = {
'cuidar_ninos':['pediatras', 'med_familiar'],
'cuidar_madre':['ginecologos'],
'cuidar_corazon_circulacion':['cardiologos', 'angiologos'],
'cuidar_pulmones_garganta':['otorrinos', 'neumologos'],
'cuidar_vejez':['geriatras'],
}




# *************************************************************
# Recomendaciones basadas en contenido de los productos:
#  - Genera recomendaciones si existen productos que por su
#    descripción numérica son similares a los que prefiere el usuario
#  - Se basa en los productos que el usuario activo a califcado
#    positivamente
#  - Recolecta productos que mediante una medida de similitud
#    sean cercanos al producto verificado como bueno
#  
# Para reconfigurar este método de recomendación: 
# 1. Determine el máximo de productos de la lista:

rec_contenido_max = 20
#
# 2. Determine el número máximo de productos similares por cada 
#    producto calificado positivamente
#
rec_contenido_k_vecinos = 2

# 3. Determine la medida de similitud: 'histogramas', 'euclidiana'
#    o 'mahalanobis'
#
rec_contenido_similitud = 'euclidiana'
#
#
#


# *************************************************************
# Recomendaciones basadas en filtrado colaborativo:
#  - Genera recomendaciones de acuerdo a los perfiles de preferencias
#    de todos los usuarios
#  - Se basa en que si los usuarios X y Y califican a N productos 
#    de forma similar, entonces ellos reaccionarán a otros productos 
#    también de forma similar 
#  
# Para reconfigurar este método de recomendación: 
# 1. Determine el máximo de productos de la lista:

rec_filtrado_colaborativo_max = 20
#
# 2. Determine la medida de similitud: 'pearson'
#
rec_filtrado_colaborativo_similitud = 'pearson'



# *************************************************************
# Recomendaciones basadas hibridas:
#  - Genera recomendaciones con base en las recomendaciones
#    por filtrado colaborativo
#  - Recomienda productos numéricamente equivalentes a los generados
#    por las recomendaciones basadas en filtrado colaborativo
#  - No tiene aspectos configurables por el usuario salvo la longitud
#	 de la lista

rec_hibrido_max = 10
#
#




