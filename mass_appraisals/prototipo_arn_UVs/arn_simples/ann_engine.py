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

from pybrain.datasets.supervised import SupervisedDataSet as SDS
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer
from pybrain.structure import FullConnection


print "hello from ann engine"




output_model_file = 'crime_model_150h_150h_sig_5000e.pkl'
train_file = 'crimerate_extract_numeric.csv'





def dicts_to_np_array(dicts):
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


	print "Numero de diccionarios: ", len(dicts)
	print "Numero de campos: ", len(input_fields)
	matrix = []
	for each_dict in dicts:
		# agregate row
		row = []
		for each_field in each_dict:
				# outputs to the left of columns
			if each_field.startswith("IM_VENTAS_VALOR"):
				row = [each_dict[each_field]] + row
			elif each_field in input_fields:
				# inputs to the rigth
				row.append(each_dict[each_field])
		matrix.append(row)
		# return numpy array
	return np.array(matrix)




def train_ann(data_dicts, layers, hidden_size, epochs):

	print "-------------------------------------------------"
 	print "loading data..."
 	# regresa un ndarray de numpy
 	train = dicts_to_np_array(data_dicts)

 	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
 	print "Spliting inputs and output for training..."

 	inputs_train = train[:,2:]
 	outputs_train = train[:,:2]
 	outputs_train = outputs_train.reshape( -1, 2 )


 	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	print "-------------------------------------------------"

 	print "primeros vectores de inputs: ", inputs_train[0:2,:]

 	print "primeros vectores de outputs: ", outputs_train[0:2,:]


 	print "Setting up supervised dataset por pyBrain training..."
 	input_size = inputs_train.shape[1]
 	target_size = outputs_train.shape[1]
 	dataset = SDS( input_size, target_size )
 	dataset.setField( 'input', inputs_train )
 	dataset.setField( 'target', outputs_train )
 	print "-------------------------------------------------"

	
 	print "Setting up network for supervised learning in pyBrain..."

 	

 	appraisal_network = FeedForwardNetwork()
 	inLayer = LinearLayer(input_size)
 	hiddenLayer1 = SigmoidLayer(hidden_size)
 	outLayer = LinearLayer(target_size)
 	appraisal_network.addInputModule(inLayer)
 	appraisal_network.addModule(hiddenLayer1)
 	appraisal_network.addOutputModule(outLayer)
 	in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
 	hidden1_to_out = FullConnection(hiddenLayer1, outLayer)
 	appraisal_network.addConnection(in_to_hidden1)
 	appraisal_network.addConnection(hidden1_to_out)
 	appraisal_network.sortModules()


 	trainer = BackpropTrainer( appraisal_network,dataset )

 	print "-------------------------------------------------"


 	rmse_vector = []
 	print "training for {} epochs...".format( epochs )
 	for i in range( epochs ):
 		mse = trainer.train()
 		rmse = sqrt( mse )
 		if i%10 == 0:
 			print "training RMSE, epoch {}: {}".format( i + 1, rmse )
 		rmse_vector.append(rmse)

 	print "-------------------------------------------------"


# 	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

 	print "Training done!"
 	print "-------------------------------------------------"

# 	return rmse_vector
	
	return appraisal_network




def train_ann_multihidden(data_dicts, layers, hidden_size, epochs):

	print "-------------------------------------------------"
 	print "loading data..."
 	# regresa un ndarray de numpy
 	train = dicts_to_np_array(data_dicts)

 	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
 	print "Spliting inputs and output for training..."

 	inputs_train = train[:,2:]
 	outputs_train = train[:,:2]
 	outputs_train = outputs_train.reshape( -1, 2 )


 	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	print "-------------------------------------------------"

 	print "primeros vectores de inputs: ", inputs_train[0:2,:]

 	print "primeros vectores de outputs: ", outputs_train[0:2,:]


 	print "Setting up supervised dataset por pyBrain training..."
 	input_size = inputs_train.shape[1]
 	target_size = outputs_train.shape[1]
 	dataset = SDS( input_size, target_size )
 	dataset.setField( 'input', inputs_train )
 	dataset.setField( 'target', outputs_train )
 	print "-------------------------------------------------"

	
	print "Setting up network for supervised learning in pyBrain..."

 	appraisal_network = FeedForwardNetwork()
 	inLayer = LinearLayer(input_size)
 	hiddenLayer1 = SigmoidLayer(hidden_size)
 	hiddenLayer2 = SigmoidLayer(hidden_size//2)
 	outLayer = LinearLayer(target_size)
 	appraisal_network.addInputModule(inLayer)
 	appraisal_network.addModule(hiddenLayer1)
 	appraisal_network.addModule(hiddenLayer2)
 	appraisal_network.addOutputModule(outLayer)
 	in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
 	hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
 	hidden2_to_out = FullConnection(hiddenLayer2, outLayer)
 	appraisal_network.addConnection(in_to_hidden1)
 	appraisal_network.addConnection(hidden1_to_hidden2)
 	appraisal_network.addConnection(hidden2_to_out)
 	appraisal_network.sortModules()


 	trainer = BackpropTrainer( appraisal_network,dataset )

 	print "-------------------------------------------------"


 	rmse_vector = []
 	print "training for {} epochs...".format( epochs )
 	for i in range( epochs ):
 		mse = trainer.train()
 		rmse = sqrt( mse )
 		print "training RMSE, epoch {}: {}".format( i + 1, rmse )
 		rmse_vector.append(rmse)

 	print "-------------------------------------------------"


# 	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

 	print "Training done!"
 	print "-------------------------------------------------"

# 	return rmse_vector
	
	return appraisal_network




def activate_network(trained_network, data_dicts):
	colors = cycle(["b", "g", "r", "c", "y", "k"])
	regression_list = []
	factual_data_list = []
	print "-------------------------------------------------"
 	print "loading data..."
 	# regresa un ndarray de numpy
 	train = dicts_to_np_array(data_dicts)

 	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
 	print "Spliting inputs and output for training..."

 	inputs_train = train[:,2:]
 	outputs_train = train[:,:2]
 	outputs_train = outputs_train.reshape( -1, 2 )

 	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	print "-------------------------------------------------"
 	print "primeros vectores de inputs: ", inputs_train[0:2,:]
 	print "primeros vectores de outputs: ", outputs_train[0:2,:]

	min_error = 0.0
	max_error = 0.0
	average_error = 0.0
	regression_list_m2 = []
	regression_list_total = []
	regression_m2_privativas = []
	factual_data_list_m2 = []
	factual_data_list_total = []

	print "loading trained model from file..."
	for i in range(inputs_train.shape[0]):
		regression = trained_network.activate(inputs_train[i])
		current_error = [abs(regression[0]-outputs_train[i][0]), abs(regression[1]-outputs_train[i][1])]
		print "   regression aproximation: ", regression,   " --> real output: ", outputs_train[i], " --> error: ", current_error
		regression_list_m2.append(regression[0])
		regression_list_total.append(regression[1])
		factual_data_list_m2.append(outputs_train[i][0])
		factual_data_list_total.append(outputs_train[i][1])

	prefix = "_simple_hidden50_epoch1500"
	labels = [i for i in range(inputs_train.shape[0])]
	fig, ax = plt.subplots()
	index = np.arange(inputs_train.shape[0])
	bar_width = 0.35
	rects1 = plt.bar(index, regression_list_total, bar_width, label="Prediccion", color=colors.next())
	rects2 = plt.bar(index + bar_width, factual_data_list_total, bar_width, label="Referencia", color=colors.next())
	plt.xticks(index + bar_width, labels)
	plt.tight_layout()
	plt.legend()
	plt.savefig("resultados_precio_total" + prefix+'.png', format='png')
	plt.close()


	labels = [i for i in range(inputs_train.shape[0])]
	fig, ax = plt.subplots()
	index = np.arange(inputs_train.shape[0])
	bar_width = 0.35
	rects1 = plt.bar(index, regression_list_m2, bar_width, label="Prediccion", color=colors.next())
	rects2 = plt.bar(index + bar_width, factual_data_list_m2, bar_width, label="Referencia", color=colors.next())
	plt.xticks(index + bar_width, labels)
	plt.tight_layout()
	plt.legend()
	plt.savefig("resultados_precio_m2" + prefix+'.png', format='png')
	plt.close()




	# appraisal_network = FeedForwardNetwork()
 	# inLayer = LinearLayer(input_size)
 	# hiddenLayer1 = TanhLayer(hidden_size)
 	# hiddenLayer2 = TanhLayer(hidden_size)
 	# hiddenLayer3 = TanhLayer(hidden_size)
 	# hiddenLayer4 = TanhLayer(hidden_size)
 	# outLayer = LinearLayer(target_size)
 	# appraisal_network.addInputModule(inLayer)
 	# appraisal_network.addModule(hiddenLayer1)
 	# appraisal_network.addModule(hiddenLayer2)
 	# appraisal_network.addModule(hiddenLayer3)
 	# appraisal_network.addModule(hiddenLayer4)
 	# appraisal_network.addOutputModule(outLayer)
 	# in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
 	# hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
 	# hidden2_to_hidden3 = FullConnection(hiddenLayer2, hiddenLayer3)
 	# hidden3_to_hidden4 = FullConnection(hiddenLayer3, hiddenLayer4)
 	# hidden4_to_out = FullConnection(hiddenLayer4, outLayer)
 	# appraisal_network.addConnection(in_to_hidden1)
 	# appraisal_network.addConnection(hidden1_to_hidden2)
 	# appraisal_network.addConnection(hidden2_to_hidden3)
 	# appraisal_network.addConnection(hidden3_to_hidden4)
 	# appraisal_network.addConnection(hidden4_to_out)
 	# appraisal_network.sortModules()

