import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import numpy as np
import cPickle as pickle
import csv
from math import sqrt
import statistics
import scipy
import os
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle
import time

from pybrain.datasets.supervised import SupervisedDataSet as SDS
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer
from pybrain.structure import FullConnection
























def dicts_to_np_array(dicts, input_fields):
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



















def train_ann(data_dicts, input_fields, hidden_size, epochs):

	#print "-------------------------------------------------"
	#print "loading data..."
	
	# regresa un ndarray de numpy
	train = dicts_to_np_array(data_dicts, input_fields)

	#print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	#print "Spliting inputs and output for training..."

	inputs_train = train[:,2:]
	outputs_train = train[:,:2]
	outputs_train = outputs_train.reshape( -1, 2 )

	#print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	#print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype

	# Setting up supervised dataset por pyBrain training...
	input_size = inputs_train.shape[1]
	target_size = outputs_train.shape[1]
	dataset = SDS( input_size, target_size )
	dataset.setField( 'input', inputs_train )
	dataset.setField( 'target', outputs_train )
	

	#Setting up network for supervised learning in pyBrain...
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

	start_time = time.time()
	rmse_vector = []
	rmse_min = sys.float_info.max
	# training for epochs...
	for i in range( epochs ):
		mse = trainer.train()
		rmse = sqrt( mse )

		# training RMSE 
		rmse_vector.append(rmse)

		if rmse < rmse_min:
			rmse_min = rmse
			#print "training RMSE, epoch {}: {}".format( i + 1, rmse )
		
	elapsed_time = time.time() - start_time

	report_fields_training = {"time_elapsed":elapsed_time, 
						"epochs":epochs,
						"rmse_min":rmse_min,
						"hidden_layers":1,
						"hidden_neurons":hidden_size,
						"input_neurons":input_size,
						"output_neurons":target_size}
	
	return report_fields_training, appraisal_network





















def activate_network(trained_network, data_dicts, input_fields):

	colors = cycle(["b", "g", "r", "c", "y", "k"])
	regression_list = []
	factual_data_list = []
	#print "-------------------------------------------------"
	#print "loading data..."
	# regresa un ndarray de numpy
	test = dicts_to_np_array(data_dicts, input_fields)

	#print "data loaded to a ", type(test),   " of size: ", test.shape, " and type:", test.dtype
	#print "Spliting inputs and output for testing..."

 	inputs_train = test[:,2:]
 	outputs_train = test[:,:2]
 	outputs_train = outputs_train.reshape( -1, 2 )

 	#print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	#print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	#print "-------------------------------------------------"
 	#print "primeros vectores de inputs: ", inputs_train[0:2,:]
 	#print "primeros vectores de outputs: ", outputs_train[0:2,:]

	
	max_error = 0.0
	average_error = 0.0
	regression_list_m2 = []
	regression_list_total = []
	regression_m2_privativas = []
	factual_data_list_m2 = []
	factual_data_list_total = []

	#"testing trained model..."
	error_min_costo_total = sys.float_info.max
	error_max_costo_total = 0
	error_promedio_costo_total = 0
	error_varianza_costo_total = 0
	error_desviacion_std_costo_total = 0
	errores_costo_total = []

	error_min_costo_m2 = sys.float_info.max
	error_max_costo_m2 = 0
	error_promedio_costo_m2 = 0
	error_varianza_costo_m2 = 0
	error_desviacion_std_costo_m2 = 0
	errores_costo_m2 = []


	for i in range(inputs_train.shape[0]):
		regression = trained_network.activate(inputs_train[i])
		
		regression_list_m2.append(regression[0])
		regression_list_total.append(regression[1])
		factual_data_list_m2.append(outputs_train[i][0])
		factual_data_list_total.append(outputs_train[i][1])

		current_error_total = abs(regression[1]-outputs_train[i][1])
		errores_costo_total.append(current_error_total)
		if current_error_total < error_min_costo_total:
			error_min_costo_total = current_error_total
		if current_error_total > error_max_costo_total:
			error_max_costo_total = current_error_total

		current_error_m2 = abs(regression[0]-outputs_train[i][0])
		errores_costo_m2.append(current_error_m2)
		if current_error_m2 < error_min_costo_m2:
			error_min_costo_m2 = current_error_m2
		if current_error_m2 > error_max_costo_m2:
			error_max_costo_m2 = current_error_m2

	promedio_costo_total = statistics.mean(factual_data_list_total)
	error_promedio_costo_total = statistics.mean(errores_costo_total)
	error_desviacion_std_costo_total = statistics.pstdev(errores_costo_total)
	error_varianza_costo_total = statistics.pvariance(errores_costo_total)

	error_promedio_costo_m2 = statistics.mean(errores_costo_m2)
	error_varianza_costo_m2 = statistics.pvariance(errores_costo_m2)
	error_desviacion_std_costo_m2 = statistics.pstdev(errores_costo_m2)
	promedio_costo_m2 = statistics.mean(factual_data_list_m2)

	report_fields_activation = {
			"Error_min_costo_total":error_min_costo_total,
			"Error_max_costo_total":error_max_costo_total,
			"Error_promedio_costo_total":error_promedio_costo_total,
			"Error_varianza_costo_total":error_varianza_costo_total,
			"Error_desviacion_std_costo_total":error_desviacion_std_costo_total,
			"Error_min_costo_m2":error_min_costo_m2,
			"Error_max_costo_m2":error_max_costo_m2,
			"Error_promedio_costo_m2":error_promedio_costo_m2,
			"Error_varianza_costo_m2":error_varianza_costo_m2,
			"Error_desviacion_std_costo_m2":error_desviacion_std_costo_m2,
			"promedio_costo_total":promedio_costo_total,
			"promedio_costo_m2":promedio_costo_m2}

	return report_fields_activation





	# prefix = "_simple_hidden50_epoch1500"
	# labels = [i for i in range(inputs_train.shape[0])]
	# fig, ax = plt.subplots()
	# index = np.arange(inputs_train.shape[0])
	# bar_width = 0.35
	# rects1 = plt.bar(index, regression_list_total, bar_width, label="Prediccion", color=colors.next())
	# rects2 = plt.bar(index + bar_width, factual_data_list_total, bar_width, label="Referencia", color=colors.next())
	# plt.xticks(index + bar_width, labels)
	# plt.tight_layout()
	# plt.legend()
	# plt.savefig("resultados_precio_total" + prefix+'.png', format='png')
	# plt.close()


	# labels = [i for i in range(inputs_train.shape[0])]
	# fig, ax = plt.subplots()
	# index = np.arange(inputs_train.shape[0])
	# bar_width = 0.35
	# rects1 = plt.bar(index, regression_list_m2, bar_width, label="Prediccion", color=colors.next())
	# rects2 = plt.bar(index + bar_width, factual_data_list_m2, bar_width, label="Referencia", color=colors.next())
	# plt.xticks(index + bar_width, labels)
	# plt.tight_layout()
	# plt.legend()
	# plt.savefig("resultados_precio_m2" + prefix+'.png', format='png')
	# plt.close()

















































































def train_ann_multihidden(data_dicts, input_fields, layers, hidden_size, epochs):

	print "-------------------------------------------------"
 	print "loading data..."
 	# regresa un ndarray de numpy
 	train = dicts_to_np_array(data_dicts, input_fields)

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

 	start_time = time.time()
 	rmse_vector = []
 	rmse_min = sys.float_info.max
 	#print "training for {} epochs...".format( epochs )
 	for i in range( epochs ):
 		mse = trainer.train()
 		rmse = sqrt( mse )
 		print "training RMSE, epoch {}: {}".format( i + 1, rmse )
 		rmse_vector.append(rmse)
 		if rmse < rmse_min:
 			rmse_min = rmse
 	#print "-------------------------------------------------"
 	elapsed_time = time.time() - start_time

# 	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

 	#print "Training done!"
 	#print "-------------------------------------------------"

# 	return rmse_vector
	
	return {"time_elapsed":elapsed_time, 
			"epochs:":epochs,
			"rmse_vector":rmse_vector,
			"rmse_min":rmse_min,
			"hidden_layers":1,
			"hidden_neurons":hidden_size
			}, appraisal_network




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

