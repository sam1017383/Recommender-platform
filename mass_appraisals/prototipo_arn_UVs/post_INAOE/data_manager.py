import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import numpy as np
import cPickle as pickle
from math import sqrt
import scipy
import os
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle

import csv
import re

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




