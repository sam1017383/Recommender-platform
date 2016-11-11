# -*- coding: utf-8 -*-
import cPickle as pickle
import random
import numpy as np
import statistics
import time
import csv
import os


import ann_engine
import data_manager
import visualizer

server='192.168.0.172'
#server='go4it.supportdesk.com.mx'
user='userAvaluos'
password='M3x1c087'
database='ExtracAvaluo'




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
						#"DISTANCIA_ESCUELAS_PRIMARIAS",
						#"DISTANCIA_UNIVERSIDAD",
						#"DISTANCIA_CENTRO_DEPORTIVO",
						#"DISTANCIA_ESCUELAS_SECUNDARIAS",
						#"DISTANCIA_CANCHAS_DEPORTIVAS",
						#"DISTANCIA_MERCADOS",
						#"DISTANCIA_SERVICIOS_SALUD_TERCER_NIVEL_",
						#"DISTANCIA_ESCUELAS_PREPARATORIA",
						#"DISTANCIA_BANCOS",
						#"DISTANCIA_LOCALES_COMERCIALES",
						#"DISTANCIA_PARQUES",
						#"DISTANCIA_PLAZASPUBLICAS",
						#"DISTANCIA_JARDINES",
						#"DISTANCIA_SUPERMERCADOS",
						#"DISTANCIA_IGLESIA",
						#"DISTANCIA_SERVICIOS_SALUD_PRIMER_NIVEL_",
						#"DISTANCIA_SERVICIOS_SALUD_SEGUNDO_NIVEL_",
						"DENSIDAD_HABITACIONAL_VIVIENDAS",
						"NUMERO_RECAMARAS",
						"NIVEL_INFRAESTRUCTURA",
						"INDICE_SATURACION_ZONA",
						"ELEVADOR",
						#"SUPERFICIE_TOTAL_CONSTRUCCIONES_PRIVATIVAS",
						#"SUPERFICIE_TOTAL_CONSTRUCCIONES_COMUNES",
						"CVE_CLASE_INMUEBLE",
						"CVE_CLASE_PRIVATIVAS",
						"CVE_ESTADO_CONSERVACION",
						"NUMERO_NIVELES",
						"NIVEL_EDIFICIO",
						"ANIO_TERMINACION_OBRA",
						#"FZO",
						#"FUB",
						#"FFR",
						#"FFO",
						#"FSU",
						#"FOT"
						]

						
output_fields = ["VALOR_FISICO_TERRENO", 
						"VALOR_FISICO_TERRENO_M2",
						"VALOR_FISICO_CONSTRUCCION",
						"IMPORTE_VALOR_CONCLUIDO"
						]






	


report_fields = ["Fecha_hora_experimento",
			"Clave_experimento",
			"Archivo_CSV_ejemplos", 
			"CP", 
			"Tiempo_entrenamiento", 
			"N_entrenamiento", 
			"N_pruebas", 
			"EPOCHS", 
			"N_neuronas_entrada",
			"N_capas_ocultas", 
			"N_neuronas_ocultas",
			"N_neuronas_salida", 
			"promedio_IMPORTE_VALOR_CONCLUIDO",
			"promedio_VALOR_FISICO_CONSTRUCCION",
			"promedio_VALOR_FISICO_TERRENO",
			"promedio_VALOR_FISICO_TERRENO_M2",
			"promedio_regresion_IMPORTE_VALOR_CONCLUIDO",
			"promedio_regresion_VALOR_FISICO_CONSTRUCCION",
			"promedio_regresion_VALOR_FISICO_TERRENO",
			"promedio_regresion_VALOR_FISICO_TERRENO_M2",
			"error_promedio_IMPORTE_VALOR_CONCLUIDO",
			"error_promedio_VALOR_FISICO_CONSTRUCCION",
			"error_promedio_VALOR_FISICO_TERRENO",
			"error_promedio_VALOR_FISICO_TERRENO_M2",
			"error_min_IMPORTE_VALOR_CONCLUIDO",
			"error_max_IMPORTE_VALOR_CONCLUIDO",
			"error_min_VALOR_FISICO_CONSTRUCCION",
			"error_max_VALOR_FISICO_CONSTRUCCION",
			"error_min_VALOR_FISICO_TERRENO",
			"error_max_VALOR_FISICO_TERRENO",
			"error_min_VALOR_FISICO_TERRENO_M2",
			"error_max_VALOR_FISICO_TERRENO_M2",
			"desviacion_std_error_IMPORTE_VALOR_CONCLUIDO",
			"desviacion_std_error_VALOR_FISICO_CONSTRUCCION",
			"desviacion_std_error_VALOR_FISICO_TERRENO",
			"desviacion_std_error_VALOR_FISICO_TERRENO_M2"
			]

report_file_name = "report_ANN_UVs_go4it_sin_normalizar_sept_2016"

# Nombre del archivo .CSV que contiene la informacion de entrenamiento y pruebas
file_name_examples = "from_server_"
#file_name = "quintanaroo_abril_2015"

# Define filtros sobre los campos del avaluo (query con la estructura (campo1=value11 or campo1=value12  or ... ) AND (campo2=value21 or campo2=value22  or ... ) 
filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240'], "CAT_TIPO_INMUEBLE":['4'], "CVE_ESTADO_CONSERVACION":['4', '5', '6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4', '5', '6'], "CVE_CLASE_INMUEBLE":['4', '5', '6'], "CAT_REGIMEN_PROPIEDAD":['1', '2', '3']}
#filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240', '03023', '03000','03020', '03023', '03600']}

#filters = {"codigo_postal_ubicacion_inmueble": ['77710', '77712', '77713', '77714', '77716', '77717', '77718', '77720', '77723', '77724', '77725', '77726' ]}
#filters = {"codigo_postal_ubicacion_inmueble": ['77710']}

#filters = {"codigo_postal_ubicacion_inmueble": ['14410']}



filter_string_msg = "-" + "-".join(filters["codigo_postal_ubicacion_inmueble"])

#filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240', '03023', '03000','03020', '03023', '03600']}

#filters = {"codigo_postal_ubicacion_inmueble": ['77710', '77712', '77713', '77714', '77716', '77717', '77718', '77720', '77723', '77724', '77725', '77726' ]}
#filters = {"codigo_postal_ubicacion_inmueble": ['77710']}

#filters = {"codigo_postal_ubicacion_inmueble": ['14410']}



filter_string_msg = "-" + "-".join(filters["codigo_postal_ubicacion_inmueble"])

filter_stm = ""
for each_field in filters:
	element = "("
	for each_value in filters[each_field]:
		element += str(each_field) + "='"+str(each_value)+"' OR "
	element = element[:-3]
	element += ")"
	filter_stm += element + " AND "

filter_stm = filter_stm[:-4]


print "filter stm: ", filter_stm

# Avaluos como una lista de diccionarios
#appraisals = data_manager.get_inputs_dicionaries(file_name_examples+'.csv', filters)
appraisals = data_manager.get_inputs_dicionaries_from_server(server, user, password, database, filter_stm, filters)

num_appraisals = len(appraisals)
generated_ints = random.sample(xrange(0,num_appraisals), num_appraisals)
appraisals_random_sorted = [appraisals[i] for i in generated_ints]

# salia a consula del primer avaluo
formated_list = visualizer.list_formated_appraisal(appraisals[0])

print "----------------------"
print "-Ejemplo de avaluo----"
for each_field in formated_list:
	print "Campo: ", each_field
print "----------------------"






# Resultados por correlacion cruzada 10-fold-cross-correlation
k = 10
data_slice = num_appraisals // k
epochs = 250

if not os.path.isfile("Experiments_log_ann_go4it.csv"):
	csvfile = open('Experiments_log_ann_go4it.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=report_fields)
	writer.writeheader()
else:
	csvfile = open('Experiments_log_ann_go4it.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=report_fields)


for hidden_size in [8]:

	#print "numero de ejemplos para entrenamiento: ", data_slice*9
	#print "numero de ejemplos para pruebas: ", data_slice
	for each_fold in range(k):
		file_prefix = file_name_examples + filter_string_msg + "_N" + str(num_appraisals) + "_E" + str(epochs) + "_10fold" + str(each_fold+1) 
		file_prefix += "_L" + str(1) + "_H" + str(hidden_size)
		print "--------------"
		print "Prefijo de experimento:", file_prefix
		exp_stats = {"Clave_experimento":file_prefix,"Archivo_CSV_ejemplos":file_name_examples,"CP":filter_stm }
	 	print "EXPERIMENT STATS:", exp_stats

		test_set = appraisals_random_sorted[each_fold*data_slice:(each_fold+1)*data_slice]
		training_set = appraisals_random_sorted[:each_fold*data_slice] + appraisals_random_sorted[(each_fold+1)*data_slice:]
		# entrenamiento de una red neuronal de una capa 
		training_stats, trained_network = ann_engine.train_ann(training_set, input_fields, output_fields, hidden_size, epochs)
		print "TRAINING STATS:", training_stats 
		# activacion de la red con los avaluos de prueba
		activations_stats = ann_engine.activate_network(trained_network, test_set , input_fields, output_fields)
		print "ACTIVATION STATS:", activations_stats 

	 	#pickle.dump(trained_network, open(file_prefix + "ANN_pybrain", 'wb'))

	 	

		
		print "error_promedio_IMPORTE_VALOR_CONCLUIDO: ", activations_stats["error_promedio_IMPORTE_VALOR_CONCLUIDO"]
		print "error_promedio_VALOR_FISICO_CONSTRUCCION: ", activations_stats["error_promedio_VALOR_FISICO_CONSTRUCCION"]
		print "error_promedio_VALOR_FISICO_TERRENO: ", activations_stats["error_promedio_VALOR_FISICO_TERRENO"]
		print "error_promedio_VALOR_FISICO_TERRENO_M2: ", activations_stats["error_promedio_VALOR_FISICO_TERRENO_M2"]


		report_values = {
				"Fecha_hora_experimento":time.strftime("%A, %d. %B %Y %I:%M%p"),
				"Clave_experimento":exp_stats["Clave_experimento"],
				"Archivo_CSV_ejemplos":exp_stats["Archivo_CSV_ejemplos"], 
				"CP":exp_stats["CP"], 
				"Tiempo_entrenamiento":training_stats["time_elapsed"], 
				"N_entrenamiento":len(training_set), 
				"N_pruebas":len(test_set), 
				"EPOCHS":training_stats["epochs"], 
				"N_neuronas_entrada":training_stats["input_neurons"],
				"N_capas_ocultas":training_stats["hidden_layers"], 
				"N_neuronas_ocultas":training_stats["hidden_neurons"],
				"N_neuronas_salida":training_stats["output_neurons"], 

				"error_min_IMPORTE_VALOR_CONCLUIDO":activations_stats["error_min_IMPORTE_VALOR_CONCLUIDO"],
				"error_max_IMPORTE_VALOR_CONCLUIDO":activations_stats["error_max_IMPORTE_VALOR_CONCLUIDO"],
				"error_min_VALOR_FISICO_CONSTRUCCION":activations_stats["error_min_VALOR_FISICO_CONSTRUCCION"],
				"error_max_VALOR_FISICO_CONSTRUCCION":activations_stats["error_max_VALOR_FISICO_CONSTRUCCION"],
				"error_min_VALOR_FISICO_TERRENO":activations_stats["error_min_VALOR_FISICO_TERRENO"],
				"error_max_VALOR_FISICO_TERRENO":activations_stats["error_max_VALOR_FISICO_TERRENO"],
				"error_min_VALOR_FISICO_TERRENO_M2":activations_stats["error_min_VALOR_FISICO_TERRENO_M2"],
				"error_max_VALOR_FISICO_TERRENO_M2":activations_stats["error_max_VALOR_FISICO_TERRENO_M2"],
				"promedio_IMPORTE_VALOR_CONCLUIDO":activations_stats["promedio_IMPORTE_VALOR_CONCLUIDO"],
				"promedio_VALOR_FISICO_CONSTRUCCION":activations_stats["promedio_VALOR_FISICO_CONSTRUCCION"],
				"promedio_VALOR_FISICO_TERRENO":activations_stats["promedio_VALOR_FISICO_TERRENO"],
				"promedio_VALOR_FISICO_TERRENO_M2":activations_stats["promedio_VALOR_FISICO_TERRENO_M2"],
				"promedio_regresion_IMPORTE_VALOR_CONCLUIDO":activations_stats["promedio_regresion_IMPORTE_VALOR_CONCLUIDO"],
				"promedio_regresion_VALOR_FISICO_CONSTRUCCION":activations_stats["promedio_regresion_VALOR_FISICO_CONSTRUCCION"],
				"promedio_regresion_VALOR_FISICO_TERRENO":activations_stats["promedio_regresion_VALOR_FISICO_TERRENO"],
				"promedio_regresion_VALOR_FISICO_TERRENO_M2":activations_stats["promedio_regresion_VALOR_FISICO_TERRENO_M2"],
				"error_promedio_IMPORTE_VALOR_CONCLUIDO":activations_stats["error_promedio_IMPORTE_VALOR_CONCLUIDO"],
				"error_promedio_VALOR_FISICO_CONSTRUCCION":activations_stats["error_promedio_VALOR_FISICO_CONSTRUCCION"],
				"error_promedio_VALOR_FISICO_TERRENO":activations_stats["error_promedio_VALOR_FISICO_TERRENO"],
				"error_promedio_VALOR_FISICO_TERRENO_M2":activations_stats["error_promedio_VALOR_FISICO_TERRENO_M2"],
				"desviacion_std_error_IMPORTE_VALOR_CONCLUIDO":activations_stats["desviacion_std_error_IMPORTE_VALOR_CONCLUIDO"],
				"desviacion_std_error_VALOR_FISICO_CONSTRUCCION":activations_stats["desviacion_std_error_VALOR_FISICO_CONSTRUCCION"],
				"desviacion_std_error_VALOR_FISICO_TERRENO":activations_stats["desviacion_std_error_VALOR_FISICO_TERRENO"],
				"desviacion_std_error_VALOR_FISICO_TERRENO_M2":activations_stats["desviacion_std_error_VALOR_FISICO_TERRENO_M2"]}
		writer.writerow(report_values)


	
	
# creacion del mapa de avaluos filtrados
visualizer.dot_infomap_from_appraisals(appraisals, "map_filtered_"+file_name_examples + filter_string_msg)












