# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import pymssql  
import cPickle as pickle
import random
from math import sqrt
from math import log
import numpy as np
import statistics
import time
import csv
import os





#server='192.168.0.172'
server='go4it.supportdesk.com.mx'
user='userAvaluos'
password='M3x1c087'
database='ExtracAvaluo'



# Define filtros sobre los campos del avaluo (query con la estructura (campo1=value11 or campo1=value12  or ... ) AND (campo2=value21 or campo2=value22  or ... ) 
#filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240'], "CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4','5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4', '5'], "CVE_CLASIFICACION_ZONA": ['2', '3']}

#coyoacan
#filters = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['003'], "CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4','5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4', '5'], "CVE_CLASIFICACION_ZONA": ['2', '3']}




# 002 Azcapotzalco
# 003 Coyoacán
# 004 Cuajimalpa de Morelos
# 005 Gustavo A. Madero
# 006 Iztacalco
# 007 Iztapalapa
# 008 La Magdalena Contreras
# 009 Milpa Alta
# 010 Álvaro Obregón
# 011 Tláhuac
# 012 Tlalpan
# 013 Xochimilco
# 014 Benito Juárez
# 015 Cuauhtémoc
# 016 Miguel Hidalgo
# 017 Venustiano Carranza



# Nombre del archivo .CSV que contiene la informacion de entrenamiento y pruebas
file_name_examples = "cdmx_depas_medio_tlalpan"
#cdmx_m1 casa habitacion 
#filters = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CAT_TIPO_INMUEBLE":['2'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']}


#cdmx_m1 casa habitacion por delegacion
filters = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['012'],"CAT_TIPO_INMUEBLE":['2'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']}


#cdmx_m1 departamentos 
#filters = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']}


#cdmx_m1 departamentos media plus
#filters = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']}




# Claves CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE
# 01 aguascalientes
# 02 baja california 
# 03 baja california sur
# 04 campeche
# 05 coahuila de zaragoza
# 06 colima
# 07 chiapas
# 08 chihuahua
# 09 df
# 10 durango
# 11 guanajuato
# 12 guerrero
# 13 hidalgo
# 14 jalisco
# 15 mexico
# 16 michoacan de ocampo
# 17 morelos
# 18 nayarit
# 19 nuevo leon
# 20 oaxaca
# 21 puebla
# 22 queretaro
# 23 quinatana roo
# 24 san luis potosi
# 25 sinaloa
# 26 sonora
# 27 tabasco
# 28 tamaulipas
# 29 tlaxcala
# 30 veracruz
# 31 yucatan
# 32 zacatecas





#
#
# Claves delegaciones

# 002 Azcapotzalco
# 003 Coyoacán
# 004 Cuajimalpa de Morelos
# 005 Gustavo A. Madero
# 006 Iztacalco
# 007 Iztapalapa
# 008 La Magdalena Contreras
# 009 Milpa Alta
# 010 Álvaro Obregón
# 011 Tláhuac
# 012 Tlalpan
# 013 Xochimilco
# 014 Benito Juárez
# 015 Cuauhtémoc
# 016 Miguel Hidalgo
# 017 Venustiano Carranza




input_fields = [ 	
					"FACTOR_RESULTANTE_PRIVATIVAS",
					"FACTOR_EDAD_PRIVATIVAS",
					"FACTOR_CONSERVACION_PRIVATIVAS",
					"CVE_ESTADO_CONSERVACION",
					"IMPORTE_ENFOQUE_INGRESOS",
					"IM_RENTAS_RENTAUNITARIA_M2",
					"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
					"NUMERO_ESTACIONAMIENTOS",
					"NUMERO_RECAMARAS",
					"SUPERFICIE_VENDIBLE",
					"SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS",
					"SUPERFICIE_PRIVATIVAS",
					"SUPERFICIE_CONSTRUIDA",
						]




select_fields = [ 	
						"LONGITUD",
						"LATITUD",
						"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE",
						"CLAVE_MUNICIPIO_UBICACION_INMUEBLE",
						"CAT_TIPO_INMUEBLE",
						"CVE_NIVEL_INFRAESTR_URBANA",
						"CVE_NIVEL_EQUIPAMIENTO_URBANO",
						"CVE_CLASE_INMUEBLE",
						"CVE_USO_CONSTRUCCION",
						"FACTOR_RESULTANTE_PRIVATIVAS",
						"FACTOR_EDAD_PRIVATIVAS",
						"FACTOR_CONSERVACION_PRIVATIVAS",
						"CVE_CLASE_GENERAL_INMUEBLES_ZONA",
						"CVE_NIVEL_SOCIO_ECONOMICO_ZONA",
						"CVE_CLASIFICACION_ZONA",
						"CVE_DENSIDAD_POBLACION",
						"CVE_REF_PROXIMIDAD_URBANA",
						"CVE_UBICACION_INMUEBLE_TERRENO",
						"DISTANCIA_UNIVERSIDAD",
						"DISTANCIA_CENTRO_DEPORTIVO",
						"DISTANCIA_CANCHAS_DEPORTIVAS",
						"DISTANCIA_MERCADOS",
						"DISTANCIA_PARQUES",
						"DISTANCIA_PLAZASPUBLICAS",
						"DISTANCIA_JARDINES",
						"DISTANCIA_SUPERMERCADOS",
						"DISTANCIA_IGLESIA",
						"NUMERO_ESTACIONAMIENTOS",
						"NUMERO_RECAMARAS",
						"SUPERFICIE_VENDIBLE",
						"FZO",
						"FFR",
						"w_avaluo2.IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
						"w_avaluo2.VALOR_COMPARATIVO_INMUEBLE_M2",
						"w_avaluo2.IMPORTE_VALOR_CONCLUIDO"
						]

select_fields_txt = [ 	
						"LONGITUD",
						"LATITUD",
						"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE",
						"CLAVE_MUNICIPIO_UBICACION_INMUEBLE",
						"CAT_TIPO_INMUEBLE",
						"CVE_NIVEL_INFRAESTR_URBANA",
						"CVE_NIVEL_EQUIPAMIENTO_URBANO",
						"CVE_CLASE_INMUEBLE",
						"CVE_USO_CONSTRUCCION",
						"FACTOR_RESULTANTE_PRIVATIVAS",
						"FACTOR_EDAD_PRIVATIVAS",
						"FACTOR_CONSERVACION_PRIVATIVAS",
						"CVE_CLASE_GENERAL_INMUEBLES_ZONA",
						"CVE_NIVEL_SOCIO_ECONOMICO_ZONA",
						"CVE_CLASIFICACION_ZONA",
						"CVE_DENSIDAD_POBLACION",
						"CVE_REF_PROXIMIDAD_URBANA",
						"CVE_UBICACION_INMUEBLE_TERRENO",
						"DISTANCIA_UNIVERSIDAD",
						"DISTANCIA_CENTRO_DEPORTIVO",
						"DISTANCIA_CANCHAS_DEPORTIVAS",
						"DISTANCIA_MERCADOS",
						"DISTANCIA_PARQUES",
						"DISTANCIA_PLAZASPUBLICAS",
						"DISTANCIA_JARDINES",
						"DISTANCIA_SUPERMERCADOS",
						"DISTANCIA_IGLESIA",
						"NUMERO_ESTACIONAMIENTOS",
						"NUMERO_RECAMARAS",
						"SUPERFICIE_VENDIBLE",
						"FZO",
						"FFR",
						"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
						"VALOR_COMPARATIVO_INMUEBLE_M2",
						"IMPORTE_VALOR_CONCLUIDO"
						]


						
output_fields = [
					"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
					"IMPORTE_VALOR_CONCLUIDO"
					]








def get_inputs_dicionaries_from_server(server, user, passw, db, filter_stm, filters, select_fields_stm):
	'load csv file to list of dictionaries'
	
	conn = pymssql.connect(server=server, user=user, password=passw, database=db)  

	cursor = conn.cursor(as_dict=True)

	query_stm = "SELECT " + select_fields_stm + " FROM w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2 WHERE " + filter_stm + " ;"

	print "Conexion iniciada con el servidor de datos"
	print "Ejecutando consulta..."
	print query_stm
	
	cursor.execute(query_stm)

	filtered_appraisals = []
	c = 1
	for row in cursor:
		new_train = {}
		inconsistency_flag = True
		for each_field in row:
			if is_num(row[each_field]):
				if c == 1:
					print "campo: ", each_field, " es numerico"
				new_train[each_field] = row[each_field]
			else:
				print "campo: ", each_field, " no es numerico"
				new_train[each_field] = '0'
				#inconsistency_flag = False
		

		if inconsistency_flag:
			filtered_appraisals.append(new_train)
			print c,"-----> INMUEBLE  agregado con ", len(new_train), "  campos"
			c += 1

	filtered_appraisals = filter_appraisals(filtered_appraisals, filters)

	
	normalised_appraisals = []
	for each_appraisal in filtered_appraisals:
		normalised_appraisals.append(normalise(each_appraisal))

	return normalised_appraisals





def is_num(s):
	if s != "" and s != None:
		try: 
			int(s)
			return True
		except ValueError:
			try: 
				float(s)
				return True
			except ValueError:
				return False
	else:
		return False




def normalise(each_appraisal):
	#print "normalizing: ", each_appraisal
	#clustering 
	#each_appraisal["codigo_postal_ubicacion_inmueble"] = str(each_appraisal["codigo_postal_ubicacion_inmueble"])
	#each_appraisal["CAT_TIPO_INMUEBLE"] = float(each_appraisal["CAT_TIPO_INMUEBLE"])
	#each_appraisal["CVE_NIVEL_INFRAESTR_URBANA"] = float(each_appraisal["CVE_NIVEL_INFRAESTR_URBANA"])
	each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"] = float(each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"])
	each_appraisal["CVE_CLASE_INMUEBLE"] = float(each_appraisal["CVE_CLASE_INMUEBLE"])
	each_appraisal["LONGITUD"] = float(each_appraisal["LONGITUD"])
	if each_appraisal["LONGITUD"] > 0:
		each_appraisal["LONGITUD"] = -1 * each_appraisal["LONGITUD"]
	each_appraisal["LATITUD"] = float(each_appraisal["LATITUD"])
	if each_appraisal["LATITUD"] < 0:
		each_appraisal["LATITUD"] = -1 * each_appraisal["LATITUD"]
	each_appraisal["CVE_USO_CONSTRUCCION"] = float(each_appraisal["CVE_USO_CONSTRUCCION"])
	#each_appraisal["GRADO_TERMINACION_OBRA"] = float(each_appraisal["GRADO_TERMINACION_OBRA"])
	#each_appraisal["AVANCE_OBRA_PRIVATIVAS"] = float(each_appraisal["AVANCE_OBRA_PRIVATIVAS"])
	each_appraisal["CVE_CLASIFICACION_ZONA"] = float(each_appraisal["CVE_CLASIFICACION_ZONA"])


	# calidad y conservacion 
	#each_appraisal["EDAD_PRIVATIVAS"] = float(each_appraisal["EDAD_PRIVATIVAS"])
	#each_appraisal["VIDA_UTIL_TOTAL_TIPO_PRIVATIVAS"] = float(each_appraisal["VIDA_UTIL_TOTAL_TIPO_PRIVATIVAS"])
	each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"] = float(each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"])
	#each_appraisal["VIDA_UTIL_REMANENTE_PRIVATIVAS"] = float(each_appraisal["VIDA_UTIL_REMANENTE_PRIVATIVAS"])
	each_appraisal["FACTOR_EDAD_PRIVATIVAS"] = float(each_appraisal["FACTOR_EDAD_PRIVATIVAS"])
	each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"] = float(each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"])
	#each_appraisal["CVE_ESTADO_CONSERVACION"] = float(each_appraisal["CVE_ESTADO_CONSERVACION"])
	#each_appraisal["CVE_CALIDAD_PROYECTO"] = float(each_appraisal["CVE_CALIDAD_PROYECTO"])

	# desarrollo urbano 
	each_appraisal["CVE_CLASE_GENERAL_INMUEBLES_ZONA"] = float(each_appraisal["CVE_CLASE_GENERAL_INMUEBLES_ZONA"])
	each_appraisal["CVE_NIVEL_SOCIO_ECONOMICO_ZONA"] = float(each_appraisal["CVE_NIVEL_SOCIO_ECONOMICO_ZONA"])
	
	each_appraisal["CVE_DENSIDAD_POBLACION"] = float(each_appraisal["CVE_DENSIDAD_POBLACION"])

	for each_field in each_appraisal:
		#print "normalizing field: ", each_field
		# evitar que la distancia desconocida sea 0
		if str(each_field).startswith("DISTANCIA"):
			each_appraisal[each_field] = float(each_appraisal[each_field])
			if each_appraisal[each_field] == 0:
				each_appraisal[each_field] = 2000
			
	# dimensiones privadas
	each_appraisal["NUMERO_ESTACIONAMIENTOS"] = float(each_appraisal["NUMERO_ESTACIONAMIENTOS"])
	each_appraisal["NUMERO_RECAMARAS"] = float(each_appraisal["NUMERO_RECAMARAS"])
	each_appraisal["SUPERFICIE_VENDIBLE"] = float(each_appraisal["SUPERFICIE_VENDIBLE"])
	#each_appraisal["SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS"] = float(each_appraisal["SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS"])
	#each_appraisal["SUPERFICIE_PRIVATIVAS"] = float(each_appraisal["SUPERFICIE_PRIVATIVAS"])
	#each_appraisal["SUPERFICIE_CONSTRUIDA"] = float(each_appraisal["SUPERFICIE_CONSTRUIDA"])


	# dimensiones comunes
	#each_appraisal["SUPERFICIE_COMUNES"] = float(each_appraisal["SUPERFICIE_COMUNES"])
	#each_appraisal["SUPERFICIE_ACCESORIA"] = float(each_appraisal["SUPERFICIE_ACCESORIA"])
	


	# salidas
	#each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"] = float(each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"])
	
	each_appraisal["IMPORTE_VALOR_CONCLUIDO"] = float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])
	
	return each_appraisal




def filter_appraisals(data, filters): 
	print "filtrando avaluos inconsistentes con precios muy bajos"
	filtered_appraisals = []
	for each_appraisal in data:
		verify = True
		for each_filter in filters:
			verify = verify and (each_appraisal[each_filter] in filters[each_filter])
		if verify and float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"]) > 400000:
			filtered_appraisals.append(each_appraisal)
		else:
			print "Se encontro un avaluo inconsistente: ", each_appraisal
	return filtered_appraisals



# 003 Coyoacán
# 004 Cuajimalpa de Morelos
# 010 Álvaro Obregón
# 012 Tlalpan
# 014 Benito Juárez
# 015 Cuauhtémoc



# filters_set = [
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['003'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['004'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['010'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['012'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['014'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['015'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
				
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['003'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['004'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['010'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['012'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['014'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['015'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '2']},
				
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['003'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['004'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['010'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['012'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['014'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'], "CLAVE_MUNICIPIO_UBICACION_INMUEBLE": ['015'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '1']},
# 				]


filters_set = [
				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3']},
				]


for filters in filters_set:
	file_name_examples = "departamentos_entidad_" + filters["CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE"][0] + "_municipio_todos_clase_4" 
	print "FILE NAME: ", file_name_examples
	filter_stm = ""
	for each_field in filters:
		element = "("
		for each_value in filters[each_field]:
			element += str(each_field) + "='"+str(each_value)+"' OR "
		element = element[:-3]
		element += ")"
		filter_stm += element + " AND "

	filter_stm = filter_stm[:-4]

	select_fields_stm = ", ".join(select_fields)




	print "filter stm: ", filter_stm

	print "select stm: ", select_fields_stm

	# Avaluos como una lista de diccionarios
	appraisals = get_inputs_dicionaries_from_server(server, user, password, database, filter_stm, filters, select_fields_stm)

	num_appraisals = len(appraisals)
	generated_ints = random.sample(xrange(0,num_appraisals), num_appraisals)
	appraisals_random_sorted = [appraisals[i] for i in generated_ints]

	# salia a consula del primer avaluo

	print "----------------------"
	print "Numero de avaluos capturados: ", num_appraisals
	print "----------------------"
	print "----------------------"
	print "-Ejemplo de avaluo----"


	f = open(file_name_examples + '.arff', 'w')
	f.write('@RELATION avaluos' + file_name_examples + '\n')

	for each_field in select_fields_txt:
		f.write('@ATTRIBUTE ' + each_field + ' NUMERIC \n')

	f.write('@DATA \n')

	for each_appraisal in appraisals_random_sorted:
		#print "----------------------"
		data = ""
		for each_field in select_fields_txt:
			#print "Campo: ", each_field, "  Valor: ",each_appraisal[each_field] 
			data = data + str(each_appraisal[each_field]) + ", "
		data = data[0:-2] + ' \n' 
		f.write(data)
		#print "----------------------", data

	f.close()






