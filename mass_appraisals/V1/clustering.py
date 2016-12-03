# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import cPickle as pickle
import random
from math import sqrt
from math import log
import numpy as np
import statistics
import time
import csv
import os

class cluster():

	fields = [ 	
			"LONGITUD",
			"LATITUD",
			"SUPERFICIE_VENDIBLE",
			"NUMERO_ESTACIONAMIENTOS",
			"NUMERO_RECAMARAS",
			"FACTOR_RESULTANTE_PRIVATIVAS",
			"FACTOR_EDAD_PRIVATIVAS",
			"FACTOR_CONSERVACION_PRIVATIVAS",
			"CVE_NIVEL_INFRAESTR_URBANA",
			"CVE_NIVEL_EQUIPAMIENTO_URBANO",
			"CVE_CLASE_INMUEBLE",
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
			"FZO",
			"FFR",
			"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
			"VALOR_COMPARATIVO_INMUEBLE_M2",
			"IMPORTE_VALOR_CONCLUIDO"
			]

	def update_statistics(self):
		print "----> stats: num avaluos in : ", self.id, len(self.avaluos)
		print "----> saving arff"
		self.save_arff()
		self.save_csv()

	def save_arff(self):
		f = open(self.id + '.arff', 'w')
		f.write('@RELATION avaluos' + self.id + '\n')
		for each_field in self.fields:
			f.write('@ATTRIBUTE ' + each_field + ' NUMERIC \n')
		f.write('@DATA \n')
		for each_appraisal in self.avaluos:
			#print "----------------------"
			data = ""
			for each_field in self.fields:
				#print "Campo: ", each_field, "  Valor: ",each_appraisal[each_field] 
				data = data + str(each_appraisal[each_field]) + ", "
			data = data[0:-2] + ' \n'
			f.write(data)
		f.close()


	def save_csv(self):
		f = open(self.id + '.csv', 'w')
		data = ""
		for each_field in self.fields:
			data = data + each_field + ", "
		data = data[0:-2] + ' \n'
		f.write(data)
		for each_appraisal in self.avaluos:
			#print "----------------------"
			data = ""
			for each_field in self.fields:
				#print "Campo: ", each_field, "  Valor: ",each_appraisal[each_field] 
				data = data + str(each_appraisal[each_field]) + ", "
			data = data[0:-2] + ' \n'
			f.write(data)
		f.close()


	def __init__(self, str_id):
		self.id = str_id
		self.avaluos = []



class clustering_engine():

	# calcula la posicion de los clusters dado conjunto de avaluos
	# prefijo: String, cadena que indica el tipo de avaluos que contiene el conjunto de avaluos
	# Avaluos: lista de diccionarios, cada dict con las caracteristicas de cada inmueble
	# num_clusters: entero, numero de grupos en los que se dividirá el conjunto
	# iterations: entero, numero de iteraciones para calcular los clusters (100-200)
	# homologation: bool, indica si se usará una distancia alternativa a la euclidiana
	def get_clusters(self, prefijo, avaluos, num_clusters, iterations, homologation):
		x = [e["LONGITUD"] for e in avaluos]
		y = [e["LATITUD"] for e in avaluos]
		num_points = len(x)
		x_min = min(x)
		y_min = min(y)
		x_max = max(x)
		y_max = max(y)
		clusters = []

		# Inicializa los clusters (posicion de las antenas) en puntos aleatorios 
		for i in range(num_clusters):
			clusters.append({"CLUSTER_ID":"id_"+str(i), "LATITUD":random.uniform(y_min, y_max), "LONGITUD":random.uniform(x_min, x_max)})
		# iterativamente recalcula los centros de los clusters 
		for i in range(iterations):
			# cada avaluo se asocia con el cluster que tenga mas proxima
			print "calculando clusters en iteracion: ", i
			asignation_mat = self.get_min_asignation_matrix(avaluos, clusters, homologation)
			# cada cluster se recalcula como el promedio de los puntos de prueba asociados
			clusters = self.get_clusters_stats(avaluos, asignation_mat, num_clusters)
		asignation_mat = self.get_min_asignation_matrix(avaluos, clusters, homologation)

		clusters_objs = self.get_clusters_objs(prefijo, avaluos, asignation_mat, num_clusters)

		return clusters_objs


	# cada cluster se recalcula como el promedio de los puntos de prueba asociados
	def get_clusters_stats(self, avaluos, asignation_mat, num_clusters):
		x = [e["LONGITUD"] for e in avaluos]
		y = [e["LATITUD"] for e in avaluos]
		num_points = len(x)
		x_min = min(x)
		y_min = min(y)
		x_max = max(x)
		y_max = max(y)
		sums_long = [0]*num_clusters
		sums_lat = [0]*num_clusters
		num_inmuebles_asociados = [0]*num_clusters
		inmuebles_asociados = [[]]*num_clusters
		counts = [0]*num_clusters

		for i, each_appraisal in enumerate(avaluos):
			for c in range(num_clusters):
				if asignation_mat[i][c]:
					sums_lat[c] += each_appraisal["LATITUD"]
					sums_long[c] += each_appraisal["LONGITUD"]
					num_inmuebles_asociados[c] += 1
					counts[c] += 1
		new_clusters = []
		for i in range(num_clusters):
			if counts[i] != 0:
				new_clusters.append({"CLUSTER_ID":"id_"+str(i), 
										"LATITUD":sums_lat[i]/num_inmuebles_asociados[i], 
										"LONGITUD":sums_long[i]/num_inmuebles_asociados[i],
										"NUM_INMUEBLES_ASOCIADOS":num_inmuebles_asociados[i]})
			else:
				# en caso de que una antena no tiene asociado ningun punto de prueba
				# se asigna nuevo cluster aleatorio
				new_clusters.append({"CLUSTER_ID":"id_"+str(i), "LATITUD":random.uniform(y_min, y_max), "LONGITUD":random.uniform(x_min, x_max)})
				
		return new_clusters




	# cada punto de prueba se asocia con la antena que tenga mas proxima
	def get_min_asignation_matrix(self, avaluos, clusters, homologation):
		# la matrix de asgnacion sera de N x C donde N es el numero de puntos de prueba
		# y C el numero de antenas o clusters
		asignation_mat = {}
		# itera por cada componente x de cada punto 
		for i, each_appraisal in enumerate(avaluos):
			c_min = 0
			c_min_distance = 1000000

			asignation_mat[i] = {}
			for c, each_cluster in enumerate(clusters):
				asignation_mat[i][c] = False
				if homologation:
					print "por hacer: homologacion"
					d = 0
				else:
					d = self.get_distance([each_appraisal["LONGITUD"], each_appraisal["LATITUD"]], [each_cluster["LONGITUD"], each_cluster["LATITUD"]])
				
				if d < c_min_distance:
					c_min_distance = d
					c_min = c	
			asignation_mat[i][c_min] = True
		return asignation_mat


	# calculo de distancia euclidiana
	def get_distance(self, point_a, point_b):
		# NOTA: en decimales GPS 1 grad = 111,320 m
		return sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)*111320



	# integra objetos tipo cluster
	def get_clusters_objs(self, prefijo, avaluos, asignation_mat, num_clusters):

		cluster_list = []
		for c in range(num_clusters):
			cltr = cluster(prefijo+str(c))
			cluster_list.append(cltr)

		for i, each_appraisal in enumerate(avaluos):
			for c in range(num_clusters):
				if asignation_mat[i][c]:
					cluster_list[c].avaluos.append(each_appraisal)
		
		for each_cluster in cluster_list:
			each_cluster.update_statistics()	
		return cluster_list



