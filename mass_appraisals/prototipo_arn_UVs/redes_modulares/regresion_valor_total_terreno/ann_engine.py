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





















def dicts_to_np_array(dicts, input_fields, output_fields):
	matrix = []
	order_1 = []
	order = []
	for each_dict in dicts:
		order = []
		# agregate row
		row = []
		for each_field in each_dict:
				# outputs to the left of columns
			if each_field in output_fields:
				if each_field not in order:
					order = [each_field] + order
				row = [each_dict[each_field]] + row
			elif each_field in input_fields:
				if each_field not in order:
					order.append(each_field)
				# inputs to the rigth
				row.append(each_dict[each_field])
		matrix.append(row)
		# return numpy array

		if order_1 == []:
			order_1 = order
			#print "Orden en el vector de avaluo: ", str(order)
		if order != order_1:
			print "Cuidado! los diccionarios se leyeron en distinto orden al vector de entrada!"

	print "NUMPY ORDER: ---->", order
	return np.array(matrix)



















def train_ann(data_dicts, input_fields, output_fields, hidden_size, epochs):

	print "-------------------------------------------------"
	print "loading data..."
	
	# regresa un ndarray de numpy
	train = dicts_to_np_array(data_dicts, input_fields, output_fields)

	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	print "Spliting inputs and output for training..."

	inputs_train = train[:,len(output_fields):]
	outputs_train = train[:,:len(output_fields)]
	outputs_train = outputs_train.reshape( -1, len(output_fields) )

	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype

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


	trainer = BackpropTrainer( appraisal_network,dataset, learningrate=0.01 )

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
			print "training RMSE, epoch {}: {}".format( i + 1, rmse )
		
	elapsed_time = time.time() - start_time

	report_fields_training = {"time_elapsed":elapsed_time, 
						"epochs":epochs,
						"rmse_min":rmse_min,
						"hidden_layers":1,
						"hidden_neurons":hidden_size,
						"input_neurons":input_size,
						"output_neurons":target_size}
	
	return report_fields_training, appraisal_network





















def activate_network(trained_network, data_dicts, input_fields, output_fields):

	colors = cycle(["b", "g", "r", "c", "y", "k"])
	regression_list = []
	factual_data_list = []
	#print "-------------------------------------------------"
	#print "loading data..."
	# regresa un ndarray de numpy
	test = dicts_to_np_array(data_dicts, input_fields, output_fields)

	#print "data loaded to a ", type(test),   " of size: ", test.shape, " and type:", test.dtype
	#print "Spliting inputs and output for testing..."

 	inputs_train = test[:,len(output_fields):]
 	outputs_train = test[:,:len(output_fields)]
 	outputs_train = outputs_train.reshape( -1, len(output_fields) )

 	#print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	#print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	#print "-------------------------------------------------"
 	#print "primeros vectores 4 de inputs: ", inputs_train[0:4,:]
 	#print "primeros vectores 4 de outputs: ", outputs_train[0:4,:]

	
	regression_list = []

	factual_data_list = []

	errors_list = []
	

	#"testing trained model..."
	error_min = sys.float_info.max

	error_max = 0

	error_avg = 0

	error_dstd = 0


	for i in range(inputs_train.shape[0]):
		regression = trained_network.activate(inputs_train[i])
		print "REGRESION: ", regression
		regression_list.append(regression[0])
		factual_data_list.append(outputs_train[i][0])
		current_error = abs(regression[0] - outputs_train[i][0])
		print "ERROR: ", int(current_error)
		errors_list.append(current_error)

		if current_error < error_min:
			error_min = current_error
		if current_error > error_max:
			error_max = current_error
		
		




	promedio_factual = statistics.mean(factual_data_list)

	promedio_regresion = statistics.mean(regression_list)

	error_avg = statistics.mean(errors_list)

	error_dstd = statistics.pstdev(factual_data_list, promedio_factual)

	report_fields_activation = {
			"error_min":error_min,
			"error_max":error_max,
			"promedio_factual":promedio_factual,
			"promedio_regresion":promedio_regresion,
			"error_avg":error_avg,
			"error_dstd":error_dstd,
			}

	return report_fields_activation



















































































def train_ann_multihidden(data_dicts, input_fields, output_fields, layers, hidden_size, epochs):

	print "-------------------------------------------------"
 	print "loading data..."
 	# regresa un ndarray de numpy
 	train = dicts_to_np_array(data_dicts, input_fields, output_fields)

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

