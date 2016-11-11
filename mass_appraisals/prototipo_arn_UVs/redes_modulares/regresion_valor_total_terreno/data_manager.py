# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import numpy as np
import cPickle as pickle
from math import sqrt
from math import log
import scipy
import os
import random
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import pymssql  

import csv
import re






# Cat.ClasesConstruccion  
# 0 NO APLICA
# 1 Mínima
# 2 Económica
# 3 Interés Social
# 4 Media
# 5 Semilujo
# 6 Residencial
# 7 Residencial Plus
# 7 Residencial Plus +
# 8 Única


# Cat.NivelInfraestructura  
# 1 No tiene alguno de los tres servicios básicos del nivel 2
# 2 Cuenta con agua potable, drenaje y luz en la zona
# 3 Cuenta con alumbrado público y vialidades terminadas (con banquetas) además de los servicios del nivel 2
# 4 Cuenta con gas natural y vigilancia privada además de los servicios del nivel 3.



# Cat.EstadoConservacion  
# 0 NO APLICA
# 1 RUINOSO
# 2 MALO
# 3 REGULAR
# 4 BUENO
# 5 MUY BUENO
# 6 NUEVO
# 7 RECIENTEMENTE REMODELADO



# Cat.NivelSocioeconomico 
# 0 No aplica
# 1 E Más bajo
# 2 D Bajo
# 3 D+ Medio Bajo
# 4 C Medio
# 5 C+ Medio Alto
# 6 A/B Alto


# Cat.NivelEquipamiento 
# 1 CUANDO EN LA ZONA EXISTAN DOS ELEMENTOS O MENOS DEL NIVEL 2.
# 2 CUANDO LA ZONA CUENTE CON  IGLESIA, MERCADO O COMERCIOS, ESCUELAS Y PARQUES Y JARDINES.
# 3 CUANDO LA ZONA TENGA LOS ELEMENTOS  DEL NIVEL 2 MÁS ACCESO O ESTACIÓN  DE TRANSPORTE PÚBLICO
# 4 CUANDO EN LA ZONA SE ENCUENTREN LOS ELEMENTOS DEL NIVEL 3 MÁS HOSPITALES Y BANCOS, MÁS OTROS EQUIPAMIENTOS



# Cat.DensidadHabitacional  
# 0 No aplica
# 1 Muy baja, 10 hab/ha una vivienda por lote de 1,000 m² 
# 2 Baja, 50 hab/ha una vivienda por lote de 500 m² 
# 3 Baja, 100 a 200 hab/ha una vivienda por lote de 250 m² 
# 4 Media, 400 hab/ha una vivienda por lote de 125 m² 
# 5 Alta, 800 hab/ha 


# Cat.Regimen 
# 1 PRIVADA
# 2 CONDOMINAL
# 3 COPROPIEDAD
# 4 PÚBLICA

# Cat.TipoInmueble  
# 1 TERRENO
# 2 CASA HABITACIÓN
# 3 CASA EN CONDOMINIO
# 4 DEPARTAMENTO EN CONDOMINIO
# 5 OTRO




output_fields = [
					"TOTAL_VALOR_TERRENO",
					"VALOR_TOTAL_CONSTRUCCIONES_PRIVATIVAS",
					"IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2",
					"IMPORTE_TOTAL_INSTALACIONES_ACCESORIOS_COMPLEMENTARIAS_COMUNES",
					"IMPORTE_INDIVISO_INSTALACIONES_ESPECIALES_OBRAS_COMPLEMENTARIAS_Y_ELEMENTOS_ACCESORIOS_COMUNES",
					"IMPORTE_VALOR_CONCLUIDO"
					]








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

def get_inputs_dicionaries_from_server(server, user, passw, db, filter_stm, filters):
	'load csv file to list of dictionaries'
	
	conn = pymssql.connect(server=server, user=user, password=passw, database=db)  

	cursor = conn.cursor(as_dict=True)

	print "Conexion iniciada con el servidor de datos"
	print "Ejecutando consulta..."
	# cursor.execute("""Select 
	# 					CVE_CLASE_INMUEBLE,
	# 					CVE_ESTADO_CONSERVACION,
	# 					CVE_DENSIDAD_HABITACIONAL,
	# 					CVE_NIVEL_SOCIO_ECONOMICO_ZONA,
	# 					CVE_NIVEL_INFRAESTR_URBANA,
	# 					CVE_NIVEL_EQUIPAMIENTO_URBANO,
	# 					CAT_REGIMEN_PROPIEDAD,
	# 					CAT_TIPO_INMUEBLE,
	# 					NUMERO_RECAMARAS,
	# 					NUMERO_BANIOS,
	# 					NUMERO_MEDIOS_BANOS,
	# 					NUMERO_ESTACIONAMIENTOS,
	# 					ELEVADOR,
	# 					INDICE_SATURACION_ZONA,
	# 					DENSIDAD_HABITACIONAL_VIVIENDAS,
	# 					NIVEL_INFRAESTRUCTURA,
	# 					DISTANCIA_IGLESIA,
	# 					DISTANCIA_BANCOS,
	# 					DISTANCIA_CANCHAS_DEPORTIVAS,
	# 					DISTANCIA_CENTRO_DEPORTIVO,
	# 					DISTANCIA_PLAZASPUBLICAS,
	# 					DISTANCIA_PARQUES,
	# 					DISTANCIA_JARDINES,
	# 					DISTANCIA_MERCADOS,
	# 					DISTANCIA_SUPERMERCADOS,
	# 					DISTANCIA_LOCALES_COMERCIALES,
	# 					DISTANCIA_SERVICIOS_SALUD_PRIMER_NIVEL_,
	# 					DISTANCIA_SERVICIOS_SALUD_SEGUNDO_NIVEL_,
	# 					DISTANCIA_SERVICIOS_SALUD_TERCER_NIVEL_,
	# 					DISTANCIA_ESCUELAS_PRIMARIAS,
	# 					DISTANCIA_ESCUELAS_SECUNDARIAS,
	# 					DISTANCIA_ESCUELAS_PREPARATORIA,
	# 					DISTANCIA_UNIVERSIDAD,
	# 					LONGITUD,
	# 					LATITUD,
	# 					codigo_postal_ubicacion_inmueble,
	# 					SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS,
	# 					SUPERFICIE_TOTAL_CONSTRUCCIONES_COMUNES,
	# 					CVE_CLASE_PRIVATIVAS,
	# 					NUMERO_NIVELES,
	# 					NIVEL_EDIFICIO,
	# 					ANIO_TERMINACION_OBRA,
	# 					FZO,
	# 					FUB,
	# 					FFR,
	# 					FFO,
	# 					FSU,
	# 					FOT,
	# 					w_avaluo2.VALOR_FISICO_TERRENO,
	# 					w_avaluo2.VALOR_FISICO_TERRENO_M2,
	# 					w_avaluo2.VALOR_FISICO_CONSTRUCCION,
	# 					w_avaluo2.IMPORTE_VALOR_CONCLUIDO
	# 				From w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2
	# 			Where """ + filter_stm + """
	# 			;
	# 			""")

	# cursor.execute("""Select 
	# 					CVE_CLASE_INMUEBLE,
	# 					CVE_ESTADO_CONSERVACION,
	# 					CVE_DENSIDAD_HABITACIONAL,
	# 					CVE_NIVEL_SOCIO_ECONOMICO_ZONA,
	# 					CVE_NIVEL_INFRAESTR_URBANA,
	# 					CVE_NIVEL_EQUIPAMIENTO_URBANO,
	# 					CAT_REGIMEN_PROPIEDAD,
	# 					CAT_TIPO_INMUEBLE,
	# 					NUMERO_RECAMARAS,
	# 					NUMERO_BANIOS,
	# 					NUMERO_MEDIOS_BANOS,
	# 					NUMERO_ESTACIONAMIENTOS,
	# 					ELEVADOR,
	# 					INDICE_SATURACION_ZONA,
	# 					DENSIDAD_HABITACIONAL_VIVIENDAS,
	# 					NIVEL_INFRAESTRUCTURA,
	# 					LONGITUD,
	# 					LATITUD,
	# 					codigo_postal_ubicacion_inmueble,
	# 					SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS,
	# 					SUPERFICIE_TOTAL_CONSTRUCCIONES_COMUNES,
	# 					CVE_CLASE_PRIVATIVAS,
	# 					NUMERO_NIVELES,
	# 					NIVEL_EDIFICIO,
	# 					ANIO_TERMINACION_OBRA,
	# 					w_avaluo2.VALOR_FISICO_TERRENO,
	# 					w_avaluo2.VALOR_FISICO_TERRENO_M2,
	# 					w_avaluo2.VALOR_FISICO_CONSTRUCCION,
	# 					w_avaluo2.IMPORTE_VALOR_CONCLUIDO
	# 				From w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2
	# 			Where """ + filter_stm + """
	# 			;
	# 			""")



	cursor.execute("""Select 
						codigo_postal_ubicacion_inmueble,
						LONGITUD,
						LATITUD,
						CAT_TIPO_INMUEBLE,
						CVE_NIVEL_INFRAESTR_URBANA,
						CVE_NIVEL_EQUIPAMIENTO_URBANO,
						CVE_CLASE_INMUEBLE,
						CVE_USO_CONSTRUCCION,
						GRADO_TERMINACION_OBRA,
						AVANCE_OBRA_PRIVATIVAS,
						EDAD_PRIVATIVAS,
						VIDA_UTIL_TOTAL_TIPO_PRIVATIVAS,
						FACTOR_RESULTANTE_PRIVATIVAS,
						VIDA_UTIL_REMANENTE_PRIVATIVAS,
						FACTOR_EDAD_PRIVATIVAS,
						FACTOR_CONSERVACION_PRIVATIVAS,
						CVE_ESTADO_CONSERVACION,
						CVE_CALIDAD_PROYECTO,
						CVE_CLASE_GENERAL_INMUEBLES_ZONA,
						CVE_NIVEL_SOCIO_ECONOMICO_ZONA,
						CVE_CLASIFICACION_ZONA,
						CVE_DENSIDAD_POBLACION,
						NUMERO_ESTACIONAMIENTOS,
						NUMERO_RECAMARAS,
						FRE,
						SUPERFICIE_VENDIBLE,
						SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS,
						SUPERFICIE_PRIVATIVAS,
						SUPERFICIE_CONSTRUIDA,
						SUPERFICIE_COMUNES,
						SUPERFICIE_ACCESORIA,
						w_avaluo2.IMPORTE_ENFOQUE_INGRESOS,
						w_avaluo2.IM_RENTAS_RENTAUNITARIA_M2,
						w_avaluo2.IMPORTE_TOTAL_ENFOQUE_DE_COSTOS,
						TOTAL_VALOR_TERRENO,
						VALOR_TOTAL_CONSTRUCCIONES_PRIVATIVAS,
						w_avaluo2.IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2,
						IMPORTE_TOTAL_INSTALACIONES_ACCESORIOS_COMPLEMENTARIAS_COMUNES,
						IMPORTE_INDIVISO_INSTALACIONES_ESPECIALES_OBRAS_COMPLEMENTARIAS_Y_ELEMENTOS_ACCESORIOS_COMUNES,
						w_avaluo2.IMPORTE_VALOR_CONCLUIDO

					From w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2
				Where """ + filter_stm + """
				;
				""")




	
	filtered_appraisals = []
	c = 1
	for row in cursor:
		new_train = {}
		inconsistency_flag = True
		for each_field in row:
			if is_num(row[each_field]):
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

	print " avalUO:::: ", filtered_appraisals[0]
	normalised_appraisals = []
	for each_appraisal in filtered_appraisals:
		normalised_appraisals.append(normalise(each_appraisal))

	return normalised_appraisals



def load_csv(csv_file):
	'load csv file to list of dictionaries'
	try:
		data = []
		raw_data = csv.DictReader(open(csv_file))
		#print "Data loaded!", raw_data
		for each_row in raw_data:
			data.append(each_row)
		return data
	except ValueError:
		print "Error: " + str(ValueError)	
		return []



def get_inputs_dicionaries(csv_file, filters):
	'load csv file to list of dictionaries'
	try:
		data = []
		raw_data = csv.DictReader(open(csv_file))
		#print "Data loaded!", raw_data
		for each_row in raw_data:
			data.append(each_row)
	except ValueError:
		print "Error: " + str(ValueError)	
		return []

	filtered_appraisals = filter_appraisals(data, filters)

	normalised_appraisals = []
	for each_appraisal in filtered_appraisals:
		normalised_appraisals.append(normalise(each_appraisal))

	return normalised_appraisals


def filter_appraisals(data, filters): 
	filtered_appraisals = []
	for each_appraisal in data:
		verify = True
		for each_filter in filters:
			verify = verify and (each_appraisal[each_filter] in filters[each_filter])
		if verify and float( each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"]) > 20000 and float(each_appraisal["IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2"]) > 10000 and float(each_appraisal["IM_RENTAS_RENTAUNITARIA_M2"]) > 20 and float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"]) > 400000:
			filtered_appraisals.append(each_appraisal)
		else:
			print "Se encontro un avaluo inconsistente: ", each_appraisal
	return filtered_appraisals

def normalise(each_appraisal):
	#print "normalizing: ", each_appraisal
	#clustering 
	each_appraisal["codigo_postal_ubicacion_inmueble"] = str(each_appraisal["codigo_postal_ubicacion_inmueble"])
	each_appraisal["CAT_TIPO_INMUEBLE"] = float(each_appraisal["CAT_TIPO_INMUEBLE"])
	each_appraisal["CVE_NIVEL_INFRAESTR_URBANA"] = float(each_appraisal["CVE_NIVEL_INFRAESTR_URBANA"])
	each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"] = float(each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"])
	each_appraisal["CVE_CLASE_INMUEBLE"] = float(each_appraisal["CVE_CLASE_INMUEBLE"])
	each_appraisal["LONGITUD"] = float(each_appraisal["LONGITUD"])
	each_appraisal["LATITUD"] = float(each_appraisal["LATITUD"])
	each_appraisal["CVE_USO_CONSTRUCCION"] = float(each_appraisal["CVE_USO_CONSTRUCCION"])
	each_appraisal["GRADO_TERMINACION_OBRA"] = float(each_appraisal["GRADO_TERMINACION_OBRA"])
	each_appraisal["AVANCE_OBRA_PRIVATIVAS"] = float(each_appraisal["AVANCE_OBRA_PRIVATIVAS"])

	# calidad y conservacion 
	each_appraisal["EDAD_PRIVATIVAS"] = float(each_appraisal["EDAD_PRIVATIVAS"])
	each_appraisal["VIDA_UTIL_TOTAL_TIPO_PRIVATIVAS"] = float(each_appraisal["VIDA_UTIL_TOTAL_TIPO_PRIVATIVAS"])
	each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"] = float(each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"])
	each_appraisal["VIDA_UTIL_REMANENTE_PRIVATIVAS"] = float(each_appraisal["VIDA_UTIL_REMANENTE_PRIVATIVAS"])
	each_appraisal["FACTOR_EDAD_PRIVATIVAS"] = float(each_appraisal["FACTOR_EDAD_PRIVATIVAS"])
	each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"] = float(each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"])
	each_appraisal["CVE_ESTADO_CONSERVACION"] = float(each_appraisal["CVE_ESTADO_CONSERVACION"])/7
	each_appraisal["CVE_CALIDAD_PROYECTO"] = float(each_appraisal["CVE_CALIDAD_PROYECTO"])/3

	# desarrollo urbano 
	each_appraisal["CVE_CLASE_GENERAL_INMUEBLES_ZONA"] = float(each_appraisal["CVE_CLASE_GENERAL_INMUEBLES_ZONA"])
	each_appraisal["CVE_NIVEL_SOCIO_ECONOMICO_ZONA"] = float(each_appraisal["CVE_NIVEL_SOCIO_ECONOMICO_ZONA"])
	each_appraisal["CVE_CLASIFICACION_ZONA"] = float(each_appraisal["CVE_CLASIFICACION_ZONA"])
	each_appraisal["CVE_DENSIDAD_POBLACION"] = float(each_appraisal["CVE_DENSIDAD_POBLACION"])
	
	# dimensiones privadas
	each_appraisal["NUMERO_ESTACIONAMIENTOS"] = float(each_appraisal["NUMERO_ESTACIONAMIENTOS"])/2
	each_appraisal["NUMERO_RECAMARAS"] = float(each_appraisal["NUMERO_RECAMARAS"])/2
	each_appraisal["FRE"] = float(each_appraisal["FRE"])
	each_appraisal["SUPERFICIE_VENDIBLE"] = float(each_appraisal["SUPERFICIE_VENDIBLE"])/100
	each_appraisal["SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS"] = float(each_appraisal["SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS"])/100
	each_appraisal["SUPERFICIE_PRIVATIVAS"] = float(each_appraisal["SUPERFICIE_PRIVATIVAS"])/100
	each_appraisal["SUPERFICIE_CONSTRUIDA"] = float(each_appraisal["SUPERFICIE_CONSTRUIDA"])/100


	# dimensiones comunes
	each_appraisal["SUPERFICIE_COMUNES"] = float(each_appraisal["SUPERFICIE_COMUNES"])/100
	each_appraisal["SUPERFICIE_ACCESORIA"] = float(each_appraisal["SUPERFICIE_ACCESORIA"])/100
	

	#  mercado
	each_appraisal["IMPORTE_ENFOQUE_INGRESOS"] = float(each_appraisal["IMPORTE_ENFOQUE_INGRESOS"])/float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])
	each_appraisal["IM_RENTAS_RENTAUNITARIA_M2"] = float(each_appraisal["IM_RENTAS_RENTAUNITARIA_M2"])/float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])
	each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"] = float(each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"])/float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])


	# salidas
	each_appraisal["TOTAL_VALOR_TERRENO"] = float(each_appraisal["TOTAL_VALOR_TERRENO"])
	each_appraisal["VALOR_TOTAL_CONSTRUCCIONES_PRIVATIVAS"] = float(each_appraisal["VALOR_TOTAL_CONSTRUCCIONES_PRIVATIVAS"])
	each_appraisal["IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2"] = float(each_appraisal["IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2"])
	each_appraisal["IMPORTE_TOTAL_INSTALACIONES_ACCESORIOS_COMPLEMENTARIAS_COMUNES"] = float(each_appraisal["IMPORTE_TOTAL_INSTALACIONES_ACCESORIOS_COMPLEMENTARIAS_COMUNES"])
	each_appraisal["IMPORTE_INDIVISO_INSTALACIONES_ESPECIALES_OBRAS_COMPLEMENTARIAS_Y_ELEMENTOS_ACCESORIOS_COMUNES"] = float(each_appraisal["IMPORTE_INDIVISO_INSTALACIONES_ESPECIALES_OBRAS_COMPLEMENTARIAS_Y_ELEMENTOS_ACCESORIOS_COMUNES"])
	each_appraisal["IMPORTE_VALOR_CONCLUIDO"] = float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])
	
	return each_appraisal




