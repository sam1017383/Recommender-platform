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
user='userAvaluos'
password='M3x1c087'
database='ExtracAvaluo'


report_fields = ["Fecha_experimento",
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
			"Promedio_costo_total",
			"Error_promedio_costo_total",
			"Promedio_costo_m2",
			"Error_promedio_costo_m2",
			"Error_min_costo_total",
			"Error_max_costo_total",
			"Error_varianza_costo_total",
			"Error_desviacion_std_costo_total",
			"Error_min_costo_m2",
			"Error_max_costo_m2",
			"Error_varianza_costo_m2",
			"Error_desviacion_std_costo_m2"
			]

report_file_name = "report_ANN_UVs_go4it_sin_normalizar_sept_2016"

# Nombre del archivo .CSV que contiene la informacion de entrenamiento y pruebas
file_name_examples = "from_"
#file_name = "quintanaroo_abril_2015"

# Define filtros sobre los campos del avaluo (query con la estructura (campo1=value11 or campo1=value12  or ... ) AND (campo2=value21 or campo2=value22  or ... ) 
filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240'], "CAT_TIPO_INMUEBLE":['4']}
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
hidden_size = 50
k = 10
data_slice = num_appraisals // k
epochs = 500

if not os.path.isfile("Experiments_log_ann_go4it.csv"):
	csvfile = open('Experiments_log_ann_go4it.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=report_fields)
	writer.writeheader()
else:
	csvfile = open('Experiments_log_ann_go4it.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=report_fields)


for hidden_size in range(50,51):

	#print "numero de ejemplos para entrenamiento: ", data_slice*9
	#print "numero de ejemplos para pruebas: ", data_slice
	for each_fold in range(k):
		file_prefix = file_name_examples + filter_string_msg + "_N" + str(num_appraisals) + "_E" + str(epochs) + "_10fold" + str(each_fold) 
		file_prefix += "_L" + str(1) + "_H" + str(hidden_size)
		print "--------------"
		print "Prefijo de experimento:", file_prefix
		test_set = appraisals_random_sorted[each_fold*data_slice:(each_fold+1)*data_slice]
		training_set = appraisals_random_sorted[:each_fold*data_slice] + appraisals_random_sorted[(each_fold+1)*data_slice:]
		# entrenamiento de una red neuronal de una capa 
		training_stats, trained_network = ann_engine.train_ann(training_set, data_manager.input_fields, hidden_size, epochs)


	 	pickle.dump(trained_network, open(file_prefix + "ANN_pybrain", 'wb'))

	 	exp_stats = {"Clave_experimento":file_prefix,"Archivo_CSV_ejemplos":file_name_examples,"CP":filter_string_msg }


	 	print "EXPERIMENT STATS:", exp_stats

		print "TRAINING STATS:", training_stats 
		# activacion de la red con los avaluos de prueba
		activations_stats = ann_engine.activate_network(trained_network, training_set , data_manager.input_fields)
		print "ACTIVATION STATS:", activations_stats 


		report_values = {
				"Fecha_experimento":time.strftime("%d-%m-%Y"),
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
				"Promedio_costo_total":activations_stats["promedio_costo_total"],
				"Error_promedio_costo_total":activations_stats["Error_promedio_costo_total"],
				"Promedio_costo_m2":activations_stats["promedio_costo_m2"],
				"Error_promedio_costo_m2":activations_stats["Error_promedio_costo_m2"],
				"Error_min_costo_total":activations_stats["Error_min_costo_total"],
				"Error_max_costo_total":activations_stats["Error_max_costo_total"],
				"Error_varianza_costo_total":activations_stats["Error_varianza_costo_total"],
				"Error_desviacion_std_costo_total":activations_stats["Error_desviacion_std_costo_total"],
				"Error_min_costo_m2":activations_stats["Error_min_costo_m2"],
				"Error_max_costo_m2":activations_stats["Error_max_costo_m2"],
				"Error_varianza_costo_m2":activations_stats["Error_varianza_costo_m2"],
				"Error_desviacion_std_costo_m2":activations_stats["Error_desviacion_std_costo_m2"]}
		writer.writerow(report_values)


	
	
# creacion del mapa de avaluos filtrados
visualizer.dot_infomap_from_appraisals(appraisals, "map_filtered_"+file_name_examples + filter_string_msg)












