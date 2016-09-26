import ann_engine

import data_manager
import visualizer

# Nombre del archivo .CSV que contiene la informacion de entrenamiento y pruebas
file_name = "cdmx_abril_2015"
#file_name = "quintanaroo_abril_2015"

# Define filtros sobre los campos del avaluo (query con la estructura (campo1=value11 or campo1=value12  or ... ) AND (campo2=value21 or campo2=value22  or ... ) 
filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240']}
#filters = {"codigo_postal_ubicacion_inmueble": ['03103', '03100', '03104', '03200', '03230', '03240', '03023', '03000','03020', '03023', '03600']}

#filters = {"codigo_postal_ubicacion_inmueble": ['77710', '77712', '77713', '77714', '77716', '77717', '77718', '77720', '77723', '77724', '77725', '77726' ]}
#filters = {"codigo_postal_ubicacion_inmueble": ['77710']}

# Avaluos como una lista de diccionarios
appraisals = data_manager.get_inputs_dicionaries(file_name+'.csv', filters)
num_appraisals = len(appraisals)
generated_ints = random.sample(xrange(0,num_appraisals), num_appraisals)
appraisals_random_sorted = [appraisals[i] for i in generated_ints]

# creacion del mapa de avaluos filtrados
visualizer.dot_infomap_from_appraisals(appraisals, "map_filtered_"+file_name)

# salia a consula del primer avaluo
formated_list = visualizer.list_formated_appraisal(appraisals[0])

print "----------------------"
print "-Ejemplo de avaluo----"
for each_field in formated_list:
	print "Campo: ", each_field
print "----------------------"

# selecciona el 80-20 para entrenamiento y pruebas






percent_80 = int(len(appraisals)*0.8)
training_app = appraisals[:percent_80]
test_app = appraisals[percent_80:]

# entrenamiento de una red neuronal de una capa 

trained_network = ann_engine.train_ann(training_app, None, hidden_size = 50, epochs = 1000)
#trained_network = ann_engine.train_ann_multihidden(training_app, None, hidden_size = 50, epochs = 1500)


# activacion de la red con los avaluos de prueba

ann_engine.activate_network(trained_network, test_app)









