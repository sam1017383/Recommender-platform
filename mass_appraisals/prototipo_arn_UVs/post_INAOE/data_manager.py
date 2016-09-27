# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import numpy as np
import cPickle as pickle
from math import sqrt
import scipy
import os
import random
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle

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


input_fields = ["CVE_CLASE_INMUEBLE", 
						"CVE_NIVEL_INFRAESTR_URBANA",
						"CVE_ESTADO_CONSERVACION",
						"CVE_NIVEL_SOCIO_ECONOMICO_ZONA",
						"CVE_NIVEL_EQUIPAMIENTO_URBANO",
						"CVE_DENSIDAD_HABITACIONAL",
						"CAT_REGIMEN_PROPIEDAD",
						"CAT_TIPO_INMUEBLE",
						"NUMERO_MEDIOS_BANOS",
						"NUMERO_RECAMARAS",
						"NUMERO_ESTACIONAMIENTOS",
						"NUMERO_BANIOS",
						"DISTANCIA_ESCUELAS_PRIMARIAS",
						"DISTANCIA_UNIVERSIDAD",
						"DISTANCIA_CENTRO_DEPORTIVO",
						"DISTANCIA_ESCUELAS_SECUNDARIAS",
						"DISTANCIA_CANCHAS_DEPORTIVAS",
						"DISTANCIA_MERCADOS",
						"DISTANCIA_SERVICIOS_SALUD_TERCER_NIVEL_",
						"DISTANCIA_ESCUELAS_PREPARATORIA",
						"DISTANCIA_BANCOS",
						"DISTANCIA_LOCALES_COMERCIALES",
						"DISTANCIA_PARQUES",
						"DISTANCIA_PLAZASPUBLICAS",
						"DISTANCIA_JARDINES",
						"DISTANCIA_SUPERMERCADOS",
						"DISTANCIA_IGLESIA",
						"DISTANCIA_SERVICIOS_SALUD_PRIMER_NIVEL_",
						"DISTANCIA_SERVICIOS_SALUD_SEGUNDO_NIVEL_",
						"DENSIDAD_HABITACIONAL_VIVIENDAS",
						"SUPERFICIE_PRIVATIVAS",
						"SUPERFICIE_TERRENO",
						"NUMERO_RECAMARAS",
						"NIVEL_INFRAESTRUCTURA",
						"INDICE_SATURACION_ZONA",
						"ELEVADOR"]
						




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



	return normalised_appraisals


def filter_appraisals(data, filters): 
	filtered_appraisals = []
	for each_appraisal in data:
		verify = True
		for each_filter in filters:
			verify = verify and (each_appraisal[each_filter] in filters[each_filter])
		if verify:
			if float(each_appraisal["IM_VENTAS_VALOR_MERCADO_INMUEBLE"]) != 0:
				filtered_appraisals.append(each_appraisal)
	return filtered_appraisals

def normalise(each_appraisal):
	#print "normalizing: ", each_appraisal
	for each_field in each_appraisal:
		#print "normalizing field: ", each_field
		# evitar que la distancia desconocida sea 0
		if str(each_field).startswith("DISTANCIA"):
			each_appraisal[each_field] = int(each_appraisal[each_field])
			if each_appraisal[each_field] == 0:
				each_appraisal[each_field] = 4000

		elif (each_field == "codigo_postal_ubicacion_inmueble" or
							each_field == "CVE_CLASE_INMUEBLE" or
							each_field == "CVE_NIVEL_INFRAESTR_URBANA" or
							each_field == "CVE_ESTADO_CONSERVACION" or
							each_field == "NUMERO_MEDIOS_BANOS" or
							each_field == "DENSIDAD_HABITACIONAL_VIVIENDAS" or
							each_field == "NUMERO_RECAMARAS" or
							each_field == "NUMERO_ESTACIONAMIENTOS" or
							each_field == "CAT_REGIMEN_PROPIEDAD" or
							each_field == "CVE_NIVEL_SOCIO_ECONOMICO_ZONA" or
							each_field == "NUMERO_RECAMARAS" or
							each_field == "CAT_TIPO_INMUEBLE" or
							each_field == "CVE_NIVEL_EQUIPAMIENTO_URBANO" or
							each_field == "CVE_DENSIDAD_HABITACIONAL" or
							each_field == "INDICE_SATURACION_ZONA" or
							each_field == "NUMERO_BANIOS" or
							each_field == "ELEVADOR"):
			each_appraisal[each_field] = int(each_appraisal[each_field])

		elif (each_field == "LATITUD" or
							each_field == "IM_VENTAS_VALOR_MERCADO_INMUEBLE" or
							each_field == "IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2" or
							each_field == "LONGITUD" or
							each_field == "SUPERFICIE_TERRENO" or
							each_field == "NIVEL_INFRAESTRUCTURA" or
							each_field == "SUPERFICIE_PRIVATIVAS"):

			each_appraisal[each_field] = float(each_appraisal[each_field])

	return each_appraisal




