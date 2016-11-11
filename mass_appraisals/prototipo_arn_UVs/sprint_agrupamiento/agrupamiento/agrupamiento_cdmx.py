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
						"GRADO_TERMINACION_OBRA",
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
						"GRADO_TERMINACION_OBRA",
						"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
						"VALOR_COMPARATIVO_INMUEBLE_M2",
						"IMPORTE_VALOR_CONCLUIDO"
						]


		




def generate_clusters(appraisals_dicts):
	markers = []
	clusters_dicts = []

	cluster = {}
	num_appraisals = len(appraisals_dicts)
	cluster["CLUSTER_ID"] = 0
	cluster["LATITUD"] = sum([e["LATITUD"] for e in appraisals_dicts])/num_appraisals
	cluster["LONGITUD"] = sum([e["LONGITUD"] for e in appraisals_dicts])/num_appraisals
	cluster["IMPORTE_VALOR_CONCLUIDO"] = sum([e["IMPORTE_VALOR_CONCLUIDO"] for e in appraisals_dicts])/num_appraisals
	cluster["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"] = sum([e["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"] for e in appraisals_dicts])/num_appraisals
	cluster["VALOR_COMPARATIVO_INMUEBLE_M2"] = sum([e["VALOR_COMPARATIVO_INMUEBLE_M2"] for e in appraisals_dicts])/num_appraisals
	cluster["SUPERFICIE_VENDIBLE"] = sum([e["SUPERFICIE_VENDIBLE"] for e in appraisals_dicts])/num_appraisals
	cluster["NUM_INMUEBLES_ASOCIADOS"] = num_appraisals
	cluster["INMUEBLES_ASOCIADOS"] = appraisals_dicts
	clusters_dicts.append(cluster)

	return clusters_dicts



# calcula la posicion de los clusters dado conjunto de avaluos,
def get_clusters(appraisals_dicts, num_clusters, iterations, homologation):
	x = [e["LONGITUD"] for e in appraisals_dicts]
	y = [e["LATITUD"] for e in appraisals_dicts]
	num_points = len(x)
	x_min = min(x)
	y_min = min(y)
	x_max = max(x)
	y_max = max(y)
	clusters = []

	# Inicializa los clusters (posicion de las antenas) en puntos aleatorios 
	for i in range(num_clusters):
		clusters.append({"CLUSTER_ID":"id_"+str(i), "LATITUD":random.uniform(y_min, y_max), "LONGITUD":random.uniform(x_min, x_max)})
	for i in range(iterations):

		print "generando clusters en iter:::::::::: ", i
		
		# cada punto de prueba se asocia con la antena que tenga mas proxima
		asignation_mat = get_min_asignation_matrix(appraisals_dicts, clusters, homologation)

		# cada cluster se recalcula como el promedio de los puntos de prueba asociados
		clusters = get_clusters_stats(appraisals_dicts, asignation_mat, num_clusters)

	asignation_mat = get_min_asignation_matrix(appraisals_dicts, clusters, homologation)
	create_clusters_arff(appraisals_dicts, asignation_mat, num_clusters)

	return clusters



# cada cluster se recalcula como el promedio de los puntos de prueba asociados
def get_clusters_stats(appraisals_dicts, asignation_mat, num_clusters):
	x = [e["LONGITUD"] for e in appraisals_dicts]
	y = [e["LATITUD"] for e in appraisals_dicts]
	num_points = len(x)
	x_min = min(x)
	y_min = min(y)
	x_max = max(x)
	y_max = max(y)
	sums_long = [0]*num_clusters
	sums_lat = [0]*num_clusters
	sums_valor_concluido = [0]*num_clusters
	sums_enfoque_costos = [0]*num_clusters
	sums_m2 = [0]*num_clusters
	num_inmuebles_asociados = [0]*num_clusters
	inmuebles_asociados = [[]]*num_clusters
	counts = [0]*num_clusters

	for i, each_appraisal in enumerate(appraisals_dicts):
		for c in range(num_clusters):
			if asignation_mat[i][c]:
				sums_lat[c] += each_appraisal["LATITUD"]
				sums_long[c] += each_appraisal["LONGITUD"]
				sums_valor_concluido[c] += each_appraisal["IMPORTE_VALOR_CONCLUIDO"]
				sums_enfoque_costos[c] += each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"]
				sums_m2[c] += each_appraisal["VALOR_COMPARATIVO_INMUEBLE_M2"]
				num_inmuebles_asociados[c] += 1
				counts[c] += 1
	new_clusters = []
	for i in range(num_clusters):
		if counts[i] != 0:
			new_clusters.append({"CLUSTER_ID":"id_"+str(i), 
									"LATITUD":sums_lat[i]/num_inmuebles_asociados[i], 
									"LONGITUD":sums_long[i]/num_inmuebles_asociados[i],
									"IMPORTE_VALOR_CONCLUIDO":sums_valor_concluido[i]/num_inmuebles_asociados[i],
									"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS":sums_enfoque_costos[i]/num_inmuebles_asociados[i],
									"VALOR_COMPARATIVO_INMUEBLE_M2":sums_m2[i]/num_inmuebles_asociados[i],
									"NUM_INMUEBLES_ASOCIADOS":num_inmuebles_asociados[i]})
		else:
			# en caso de que una antena no tiene asociado ningun punto de prueba
			# se asigna nuevo cluster aleatorio
			new_clusters.append({"CLUSTER_ID":"id_"+str(i), "LATITUD":random.uniform(y_min, y_max), "LONGITUD":random.uniform(x_min, x_max)})
			
	return new_clusters


# cada cluster se recalcula como el promedio de los puntos de prueba asociados
def create_clusters_arff(appraisals_dicts, asignation_mat, num_clusters):
	inmuebles_asociados = [[]]*num_clusters
	cuenta = [0]*num_clusters
	for i, each_appraisal in enumerate(appraisals_dicts):
		#print "asignation row: ", asignation_mat[i]
		for c in range(num_clusters):
			if asignation_mat[i][c]:
				inmuebles_asociados[c] = inmuebles_asociados[c] + [each_appraisal]
				cuenta[c] += 1
				#print "inmueble_asociado a cluster  :::::::::: ", c
				#print "cuenta: ", cuenta[c], " real: ", len(inmuebles_asociados[c])
	
	for c in range(num_clusters):
		if len(inmuebles_asociados[c]) > 100:
			file_name = "cdmx_cluster_" + str(c) + "_de_" + str(num_clusters)
			f = open(file_name + '.arff', 'w')
			f.write('@RELATION avaluos' + file_name + '\n')

			for each_field in select_fields_txt:
				f.write('@ATTRIBUTE ' + each_field + ' NUMERIC \n')

			f.write('@DATA \n')

			#print "inmuebles_asociados :::::::::: ", len(inmuebles_asociados[c])
			#print "al cluster :::::::::: ", c


			for each_app in inmuebles_asociados[c]:
				#print "----------------------"
				data = ""
				for each_field in select_fields_txt:
					#print "Campo: ", each_field, "  Valor: ",each_appraisal[each_field] 
					data = data + str(each_app[each_field]) + ", "
				data = data[0:-2] + ' \n' 
				f.write(data)
				#print "----------------------", data

			f.close()

	



# cada punto de prueba se asocia con la antena que tenga mas proxima
def get_min_asignation_matrix(appraisals_dicts, clusters, homologation):
	# la matrix de asgnacion sera de N x C donde N es el numero de puntos de prueba
	# y C el numero de antenas o clusters
	asignation_mat = {}
	# itera por cada componente x de cada punto 
	for i, each_appraisal in enumerate(appraisals_dicts):
		c_min = 0
		c_min_distance = 1000000

		asignation_mat[i] = {}
		for c, each_cluster in enumerate(clusters):
			asignation_mat[i][c] = False
			if homologation:
				print "por hacer: homologacion"
				d = 0
			else:
				d = get_distance([each_appraisal["LONGITUD"], each_appraisal["LATITUD"]], [each_cluster["LONGITUD"], each_cluster["LATITUD"]])
			
			if d < c_min_distance:
				c_min_distance = d
				c_min = c	
		asignation_mat[i][c_min] = True
	return asignation_mat


# calculo de distancia euclidiana
def get_distance(point_a, point_b):
	# NOTA: en decimales GPS 1 grad = 111,320 m
	return sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)*111320

















































def draw_appraisal_clusters(self, clusters_dicts):

	my_map = open(file_name + '.html', 'w+')
	involved_routes_code = ""
	center = ""
	colors = cycle(['#993399', '#6600ff', '#003399', '#6600ff', '#006666', '#663300', '#009999', '#00ff00', '#336600', '#996633', '#ccffcc', '#666699', '#003300'])
	for each_g in best_route_dict["routes_graphs_list"]:
		route_color = colors.next()
		for nA, nbrs in each_g.adjacency_iter():
			if center == "":
				center = "var myLatLng = {lat: "+str(each_g.node[nA]["latitud"])+ "  , lng: " + str(each_g.node[nA]["longitud"]) +" };"
			for nB, att in nbrs.items():
				involved_routes_code += """
  var sequence = [{lat: """ + str(each_g.node[nA]["latitud"]) + ", lng: "+ str(each_g.node[nA]["longitud"]) +"},{lat: "+ str(each_g.node[nB]["latitud"]) +", lng: "+ str(each_g.node[nB]["longitud"]) +"}];"+ """
  var drawable_path = new google.maps.Polyline({ path: sequence, geodesic: true, strokeColor: '"""+ route_color+ """', strokeOpacity: 1.0, strokeWeight: 2});
  drawable_path.setMap(map);
				"""
	path_code = "var sequence = ["
	end_code = """
  var drawable_path = new google.maps.Polyline({ path: sequence, geodesic: true, strokeColor: '#0ED72F', strokeOpacity: 0.5, strokeWeight: 6});
  drawable_path.setMap(map);
				"""
	for each_dot in best_route_dict["stitched_route_gps"]:
		path_code += "{lat: " + str(each_dot[1]) + ", lng: "+ str(each_dot[0]) + "},"
	path_code = path_code[:len(path_code)-1]
	path_code += "]; \n"
	path_code += end_code
	c = 0
	pins = ""
	for each_dot in best_route_dict["route_transfer_gps"]:
		pins += "var marker = new google.maps.Marker({position: {lat: " + str(each_dot[1]) + "  , lng: " + str(each_dot[0]) + " }, map: map, title: 'Transbordo!'}); \n"		
		
		pins += """
var contentString = '<div id="content">'+
'<div id="inmueble">'+
'</div>'+
'<h1 id="firstHeading" class="firstHeading"> Ruta """ +  """</h1>'+
'<div id="bodyContent">'+
'<h2> Secuencia de rutas a tomar: """ + str(best_route_dict["route_order"]) +  """ </h2>' +
'<h2> Distancia total de viaje: """ + str(best_route_dict["distance"]) +  """ metros</h2>' +
'<h3> Direcciones: """ + str(best_route_dict["directions"]) +  """ </h2>' +
'</div>'+
'</div>';
var infowindow"""+ str(c) +  """ = new google.maps.InfoWindow({
content: contentString
});
var marker"""+ str(c) +  """ = new google.maps.Marker({position: {lat: """ + str(each_dot[1]) + "  , lng: " + str(each_dot[0]) + """ }, map: map, title: 'Transbordo!'}); 
marker"""+ str(c) +  """.addListener('click', function() {
infowindow"""+ str(c) +  """.open(map, marker"""+ str(c) +  """);
});
"""
		c += 1
	code = self.html_header+center+self.gmap_init+pins+involved_routes_code+path_code+self.html_end
	my_map.write(code)
	my_map.close()
	return code





















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
	each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"] = float(each_appraisal["CVE_NIVEL_EQUIPAMIENTO_URBANO"])
	each_appraisal["CVE_CLASE_INMUEBLE"] = float(each_appraisal["CVE_CLASE_INMUEBLE"])
	each_appraisal["LONGITUD"] = float(each_appraisal["LONGITUD"])
	if each_appraisal["LONGITUD"] > 0:
		each_appraisal["LONGITUD"] = -1 * each_appraisal["LONGITUD"]
	each_appraisal["LATITUD"] = float(each_appraisal["LATITUD"])
	if each_appraisal["LATITUD"] < 0:
		each_appraisal["LATITUD"] = -1 * each_appraisal["LATITUD"]
	each_appraisal["CVE_USO_CONSTRUCCION"] = float(each_appraisal["CVE_USO_CONSTRUCCION"])
	each_appraisal["CVE_CLASIFICACION_ZONA"] = float(each_appraisal["CVE_CLASIFICACION_ZONA"])


	# calidad y conservacion 
	each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"] = float(each_appraisal["FACTOR_RESULTANTE_PRIVATIVAS"])
	each_appraisal["FACTOR_EDAD_PRIVATIVAS"] = float(each_appraisal["FACTOR_EDAD_PRIVATIVAS"])
	each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"] = float(each_appraisal["FACTOR_CONSERVACION_PRIVATIVAS"])
	each_appraisal["GRADO_TERMINACION_OBRA"] = float(each_appraisal["GRADO_TERMINACION_OBRA"])
	


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

	each_appraisal["VALOR_COMPARATIVO_INMUEBLE_M2"] = float(each_appraisal["VALOR_COMPARATIVO_INMUEBLE_M2"])
	each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"] = float(each_appraisal["IMPORTE_TOTAL_ENFOQUE_DE_COSTOS"])
	each_appraisal["IMPORTE_VALOR_CONCLUIDO"] = float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"])



	
	
	return each_appraisal




def filter_appraisals(data, filters): 
	print "filtrando avaluos inconsistentes con precios muy bajos"
	filtered_appraisals = []
	for each_appraisal in data:
		verify = True
		for each_filter in filters:
			verify = verify and (each_appraisal[each_filter] in filters[each_filter])
		if verify and float(each_appraisal["IMPORTE_VALOR_CONCLUIDO"]) > 400000 and float(each_appraisal["LATITUD"]) > 19:
			filtered_appraisals.append(each_appraisal)
		else:
			print "Se encontro un avaluo inconsistente: ", each_appraisal
	return filtered_appraisals





filters_set = [
				{"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']},
				]


for filters in filters_set:
	file_name_examples = "departamentos_entidad_" + filters["CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE"][0] + "_agrupamiento_espacial" 
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


	print "----------------------"
	print "Numero de avaluos capturados: ", num_appraisals
	print "----------------------"
	if num_appraisals > 0:
		print "----------------------"
		print "Numero de avaluos capturados: ", num_appraisals
		print "----------------------AVALUO de ejemplo: ", appraisals[0]
		print "--------AGRUPAMIENTO--------------"
		clusters = get_clusters(appraisals, 100, 200, False)



		for each_cluster in clusters:
			print "----------------------CLUSTER: ", each_cluster




