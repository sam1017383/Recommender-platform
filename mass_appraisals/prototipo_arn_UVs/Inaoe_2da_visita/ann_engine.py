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

	#print "-------------------------------------------------"
	#print "loading data..."
	
	# regresa un ndarray de numpy
	train = dicts_to_np_array(data_dicts, input_fields, output_fields)

	#print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	#print "Spliting inputs and output for training..."

	inputs_train = train[:,4:]
	outputs_train = train[:,:4]
	outputs_train = outputs_train.reshape( -1, 4 )

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

 	inputs_train = test[:,4:]
 	outputs_train = test[:,:4]
 	outputs_train = outputs_train.reshape( -1, 4 )

 	#print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
 	#print "output in a ", type(outputs_train),   " of size: ", outputs_train.shape, " and type:", outputs_train.dtype
 	#print "-------------------------------------------------"
 	#print "primeros vectores 4 de inputs: ", inputs_train[0:4,:]
 	#print "primeros vectores 4 de outputs: ", outputs_train[0:4,:]

	
	regression_list_VALOR_FISICO_TERRENO = []
	regression_list_VALOR_FISICO_TERRENO_M2 = []
	regression_list_VALOR_FISICO_CONSTRUCCION = []
	regression_list_IMPORTE_VALOR_CONCLUIDO = []

	factual_data_list_VALOR_FISICO_TERRENO = []
	factual_data_list_VALOR_FISICO_TERRENO_M2 = []
	factual_data_list_VALOR_FISICO_CONSTRUCCION = []
	factual_data_list_IMPORTE_VALOR_CONCLUIDO = []

	errors_list_VALOR_FISICO_TERRENO = []
	errors_list_VALOR_FISICO_TERRENO_M2 = []
	errors_list_VALOR_FISICO_CONSTRUCCION = []
	errors_list_IMPORTE_VALOR_CONCLUIDO = []
	

	#"testing trained model..."
	error_min_VALOR_FISICO_TERRENO = sys.float_info.max
	error_min_VALOR_FISICO_TERRENO_M2 = sys.float_info.max
	error_min_VALOR_FISICO_CONSTRUCCION = sys.float_info.max
	error_min_IMPORTE_VALOR_CONCLUIDO = sys.float_info.max

	error_max_VALOR_FISICO_TERRENO = 0
	error_max_VALOR_FISICO_TERRENO_M2 = 0
	error_max_VALOR_FISICO_CONSTRUCCION = 0
	error_max_IMPORTE_VALOR_CONCLUIDO = 0

	error_avg_VALOR_FISICO_TERRENO = 0
	error_avg_VALOR_FISICO_TERRENO_M2 = 0
	error_avg_VALOR_FISICO_CONSTRUCCION = 0
	error_avg_IMPORTE_VALOR_CONCLUIDO = 0

	error_dstd_VALOR_FISICO_TERRENO = 0
	error_dstd_VALOR_FISICO_TERRENO_M2 = 0
	error_dstd_VALOR_FISICO_CONSTRUCCION = 0
	error_dstd_IMPORTE_VALOR_CONCLUIDO = 0


	for i in range(inputs_train.shape[0]):
		regression = trained_network.activate(inputs_train[i])
		
		# posiciones en el vector de salida
		IMPORTE_VALOR_CONCLUIDO = 1
		VALOR_FISICO_CONSTRUCCION = 2
		VALOR_FISICO_TERRENO = 3
		VALOR_FISICO_TERRENO_M2 = 0


		regression_list_VALOR_FISICO_TERRENO.append(regression[VALOR_FISICO_TERRENO])
		regression_list_VALOR_FISICO_TERRENO_M2.append(regression[VALOR_FISICO_TERRENO_M2])
		regression_list_VALOR_FISICO_CONSTRUCCION.append(regression[VALOR_FISICO_CONSTRUCCION])
		regression_list_IMPORTE_VALOR_CONCLUIDO.append(regression[IMPORTE_VALOR_CONCLUIDO])
		

		factual_data_list_VALOR_FISICO_TERRENO.append(outputs_train[i][VALOR_FISICO_TERRENO])
		factual_data_list_VALOR_FISICO_TERRENO_M2.append(outputs_train[i][VALOR_FISICO_TERRENO_M2])
		factual_data_list_VALOR_FISICO_CONSTRUCCION.append(outputs_train[i][VALOR_FISICO_CONSTRUCCION])
		factual_data_list_IMPORTE_VALOR_CONCLUIDO.append(outputs_train[i][IMPORTE_VALOR_CONCLUIDO])


		current_error_IMPORTE_VALOR_CONCLUIDO = abs(regression[IMPORTE_VALOR_CONCLUIDO]-outputs_train[i][IMPORTE_VALOR_CONCLUIDO])
		errors_list_IMPORTE_VALOR_CONCLUIDO.append(current_error_IMPORTE_VALOR_CONCLUIDO)
		if current_error_IMPORTE_VALOR_CONCLUIDO < error_min_IMPORTE_VALOR_CONCLUIDO:
			error_min_IMPORTE_VALOR_CONCLUIDO = current_error_IMPORTE_VALOR_CONCLUIDO
		if current_error_IMPORTE_VALOR_CONCLUIDO > error_max_IMPORTE_VALOR_CONCLUIDO:
			error_max_IMPORTE_VALOR_CONCLUIDO = current_error_IMPORTE_VALOR_CONCLUIDO


		current_error_VALOR_FISICO_CONSTRUCCION = abs(regression[VALOR_FISICO_CONSTRUCCION]-outputs_train[i][VALOR_FISICO_CONSTRUCCION])
		errors_list_VALOR_FISICO_CONSTRUCCION.append(current_error_VALOR_FISICO_CONSTRUCCION)
		if current_error_VALOR_FISICO_CONSTRUCCION < error_min_VALOR_FISICO_CONSTRUCCION:
			error_min_VALOR_FISICO_CONSTRUCCION = current_error_VALOR_FISICO_CONSTRUCCION
		if current_error_VALOR_FISICO_CONSTRUCCION > error_max_VALOR_FISICO_CONSTRUCCION:
			error_max_VALOR_FISICO_CONSTRUCCION = current_error_VALOR_FISICO_CONSTRUCCION


		current_error_VALOR_FISICO_TERRENO = abs(regression[VALOR_FISICO_TERRENO]-outputs_train[i][VALOR_FISICO_TERRENO])
		errors_list_VALOR_FISICO_TERRENO.append(current_error_VALOR_FISICO_TERRENO)
		if current_error_VALOR_FISICO_TERRENO < error_min_VALOR_FISICO_TERRENO:
			error_min_VALOR_FISICO_TERRENO = current_error_VALOR_FISICO_TERRENO
		if current_error_VALOR_FISICO_TERRENO > error_max_VALOR_FISICO_TERRENO:
			error_max_VALOR_FISICO_TERRENO = current_error_VALOR_FISICO_TERRENO



		current_error_VALOR_FISICO_TERRENO_M2 = abs(regression[VALOR_FISICO_TERRENO_M2]-outputs_train[i][VALOR_FISICO_TERRENO_M2])
		errors_list_VALOR_FISICO_TERRENO_M2.append(current_error_VALOR_FISICO_TERRENO_M2)
		if current_error_VALOR_FISICO_TERRENO_M2 < error_min_VALOR_FISICO_TERRENO_M2:
			error_min_VALOR_FISICO_TERRENO_M2 = current_error_VALOR_FISICO_TERRENO_M2
		if current_error_VALOR_FISICO_TERRENO_M2 > error_max_VALOR_FISICO_TERRENO_M2:
			error_max_VALOR_FISICO_TERRENO_M2 = current_error_VALOR_FISICO_TERRENO_M2



	promedio_IMPORTE_VALOR_CONCLUIDO = statistics.mean(factual_data_list_IMPORTE_VALOR_CONCLUIDO)
	promedio_VALOR_FISICO_CONSTRUCCION = statistics.mean(factual_data_list_VALOR_FISICO_CONSTRUCCION)
	promedio_VALOR_FISICO_TERRENO = statistics.mean(factual_data_list_VALOR_FISICO_TERRENO)
	promedio_VALOR_FISICO_TERRENO_M2 = statistics.mean(factual_data_list_VALOR_FISICO_TERRENO_M2)

	promedio_regresion_IMPORTE_VALOR_CONCLUIDO = statistics.mean(regression_list_IMPORTE_VALOR_CONCLUIDO)
	promedio_regresion_VALOR_FISICO_CONSTRUCCION = statistics.mean(regression_list_VALOR_FISICO_CONSTRUCCION)
	promedio_regresion_VALOR_FISICO_TERRENO = statistics.mean(regression_list_VALOR_FISICO_TERRENO)
	promedio_regresion_VALOR_FISICO_TERRENO_M2 = statistics.mean(regression_list_VALOR_FISICO_TERRENO_M2)

	error_promedio_IMPORTE_VALOR_CONCLUIDO = statistics.mean(errors_list_IMPORTE_VALOR_CONCLUIDO)
	error_promedio_VALOR_FISICO_CONSTRUCCION = statistics.mean(errors_list_VALOR_FISICO_CONSTRUCCION)
	error_promedio_VALOR_FISICO_TERRENO = statistics.mean(errors_list_VALOR_FISICO_TERRENO)
	error_promedio_VALOR_FISICO_TERRENO_M2 = statistics.mean(errors_list_VALOR_FISICO_TERRENO_M2)


	desviacion_std_error_IMPORTE_VALOR_CONCLUIDO = statistics.pstdev(errors_list_IMPORTE_VALOR_CONCLUIDO, error_promedio_IMPORTE_VALOR_CONCLUIDO)
	desviacion_std_error_VALOR_FISICO_CONSTRUCCION = statistics.pstdev(errors_list_VALOR_FISICO_CONSTRUCCION, error_promedio_VALOR_FISICO_CONSTRUCCION)
	desviacion_std_error_VALOR_FISICO_TERRENO = statistics.pstdev(errors_list_VALOR_FISICO_TERRENO, error_promedio_VALOR_FISICO_TERRENO)
	desviacion_std_error_VALOR_FISICO_TERRENO_M2 = statistics.pstdev(errors_list_VALOR_FISICO_TERRENO_M2, error_promedio_VALOR_FISICO_TERRENO_M2)

	report_fields_activation = {
			"error_min_IMPORTE_VALOR_CONCLUIDO":error_min_IMPORTE_VALOR_CONCLUIDO,
			"error_max_IMPORTE_VALOR_CONCLUIDO":error_max_IMPORTE_VALOR_CONCLUIDO,
			"error_min_VALOR_FISICO_CONSTRUCCION":error_min_VALOR_FISICO_CONSTRUCCION,
			"error_max_VALOR_FISICO_CONSTRUCCION":error_max_VALOR_FISICO_CONSTRUCCION,
			"error_min_VALOR_FISICO_TERRENO":error_min_VALOR_FISICO_TERRENO,
			"error_max_VALOR_FISICO_TERRENO":error_max_VALOR_FISICO_TERRENO,
			"error_min_VALOR_FISICO_TERRENO_M2":error_min_VALOR_FISICO_TERRENO_M2,
			"error_max_VALOR_FISICO_TERRENO_M2":error_max_VALOR_FISICO_TERRENO_M2,
			"promedio_IMPORTE_VALOR_CONCLUIDO":promedio_IMPORTE_VALOR_CONCLUIDO,
			"promedio_VALOR_FISICO_CONSTRUCCION":promedio_VALOR_FISICO_CONSTRUCCION,
			"promedio_VALOR_FISICO_TERRENO":promedio_VALOR_FISICO_TERRENO,
			"promedio_VALOR_FISICO_TERRENO_M2":promedio_VALOR_FISICO_TERRENO_M2,
			"promedio_regresion_IMPORTE_VALOR_CONCLUIDO":promedio_regresion_IMPORTE_VALOR_CONCLUIDO,
			"promedio_regresion_VALOR_FISICO_CONSTRUCCION":promedio_regresion_VALOR_FISICO_CONSTRUCCION,
			"promedio_regresion_VALOR_FISICO_TERRENO":promedio_regresion_VALOR_FISICO_TERRENO,
			"promedio_regresion_VALOR_FISICO_TERRENO_M2":promedio_regresion_VALOR_FISICO_TERRENO_M2,
			"error_promedio_IMPORTE_VALOR_CONCLUIDO":error_promedio_IMPORTE_VALOR_CONCLUIDO,
			"error_promedio_VALOR_FISICO_CONSTRUCCION":error_promedio_VALOR_FISICO_CONSTRUCCION,
			"error_promedio_VALOR_FISICO_TERRENO":error_promedio_VALOR_FISICO_TERRENO,
			"error_promedio_VALOR_FISICO_TERRENO_M2":error_promedio_VALOR_FISICO_TERRENO_M2,
			"desviacion_std_error_IMPORTE_VALOR_CONCLUIDO":desviacion_std_error_IMPORTE_VALOR_CONCLUIDO,
			"desviacion_std_error_VALOR_FISICO_CONSTRUCCION":desviacion_std_error_VALOR_FISICO_CONSTRUCCION,
			"desviacion_std_error_VALOR_FISICO_TERRENO":desviacion_std_error_VALOR_FISICO_TERRENO,
			"desviacion_std_error_VALOR_FISICO_TERRENO_M2":desviacion_std_error_VALOR_FISICO_TERRENO_M2}

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

