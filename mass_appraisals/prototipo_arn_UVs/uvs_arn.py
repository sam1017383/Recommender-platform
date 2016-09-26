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












































output_model_file = 'crime_model_150h_150h_sig_5000e.pkl'
train_file = 'crimerate_extract_numeric.csv'
#test_file = 'crimerate_extract_numeric_test.csv'
test_file = 'crimerate_extract_numeric.csv'

hidden_size = 150
epochs = 5000




def train_4_hidden():

	print "-------------------------------------------------"
	print "loading data..."
	print "file to be loaded: ", train_file

	# regresa un ndarray de numpy
	train = np.loadtxt( train_file, delimiter = ',' )

	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	print "Spliting inputs and output for training..."

	inputs_train = train[:,0:-1]
	output_train = train[:,-1]
	output_train = output_train.reshape( -1, 1 )


	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(output_train),   " of size: ", output_train.shape, " and type:", output_train.dtype
	print "-------------------------------------------------"



	print "Setting up supervised dataset por pyBrain training..."
	input_size = inputs_train.shape[1]
	target_size = output_train.shape[1]
	dataset = SDS( input_size, target_size )
	dataset.setField( 'input', inputs_train )
	dataset.setField( 'target', output_train )
	print "-------------------------------------------------"



	print "Setting up network for supervised learning in pyBrain..."
	
	#crime_network = buildNetwork( input_size, hidden_size, target_size, bias = True, hiddenclass = SigmoidLayer, outclass = LinearLayer )
	
	


	crime_ann = FeedForwardNetwork()

	inLayer = LinearLayer(input_size)
	hiddenLayer1 = TanhLayer(hidden_size)
	hiddenLayer2 = TanhLayer(hidden_size)
	hiddenLayer3 = TanhLayer(hidden_size)
	hiddenLayer4 = TanhLayer(hidden_size)
	outLayer = LinearLayer(target_size)
	crime_ann.addInputModule(inLayer)
	crime_ann.addModule(hiddenLayer1)
	crime_ann.addModule(hiddenLayer2)
	crime_ann.addModule(hiddenLayer3)
	crime_ann.addModule(hiddenLayer4)
	crime_ann.addOutputModule(outLayer)
	in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
	hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
	hidden2_to_hidden3 = FullConnection(hiddenLayer2, hiddenLayer3)
	hidden3_to_hidden4 = FullConnection(hiddenLayer3, hiddenLayer4)
	hidden4_to_out = FullConnection(hiddenLayer4, outLayer)
	crime_ann.addConnection(in_to_hidden1)
	crime_ann.addConnection(hidden1_to_hidden2)
	crime_ann.addConnection(hidden2_to_hidden3)
	crime_ann.addConnection(hidden3_to_hidden4)
	crime_ann.addConnection(hidden4_to_out)
	crime_ann.sortModules()


	trainer = BackpropTrainer( crime_ann,dataset )

	print "-------------------------------------------------"


	rmse_vector = []
	print "training for {} epochs...".format( epochs )
	for i in range( epochs ):
		mse = trainer.train()
		rmse = sqrt( mse )
		print "training RMSE, epoch {}: {}".format( i + 1, rmse )
		rmse_vector.append(rmse)

	print "-------------------------------------------------"
	
	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

	print "Training done!"
	print "-------------------------------------------------"

	return rmse_vector




def train_5_hidden():

	print "-------------------------------------------------"
	print "loading data..."
	print "file to be loaded: ", train_file

	# regresa un ndarray de numpy
	train = np.loadtxt( train_file, delimiter = ',' )

	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	print "Spliting inputs and output for training..."

	inputs_train = train[:,0:-1]
	output_train = train[:,-1]
	output_train = output_train.reshape( -1, 1 )


	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(output_train),   " of size: ", output_train.shape, " and type:", output_train.dtype
	print "-------------------------------------------------"



	print "Setting up supervised dataset por pyBrain training..."
	input_size = inputs_train.shape[1]
	target_size = output_train.shape[1]
	dataset = SDS( input_size, target_size )
	dataset.setField( 'input', inputs_train )
	dataset.setField( 'target', output_train )
	print "-------------------------------------------------"



	print "Setting up network for supervised learning in pyBrain..."
	
	#crime_network = buildNetwork( input_size, hidden_size, target_size, bias = True, hiddenclass = SigmoidLayer, outclass = LinearLayer )
	
	


	crime_ann = FeedForwardNetwork()

	inLayer = LinearLayer(input_size)
	hiddenLayer1 = SigmoidLayer(100)
	hiddenLayer2 = SigmoidLayer(hidden_size)
	hiddenLayer3 = SigmoidLayer(hidden_size)
	hiddenLayer4 = SigmoidLayer(hidden_size)
	hiddenLayer5 = SigmoidLayer(hidden_size)
	outLayer = LinearLayer(target_size)
	crime_ann.addInputModule(inLayer)
	crime_ann.addModule(hiddenLayer1)
	crime_ann.addModule(hiddenLayer2)
	crime_ann.addModule(hiddenLayer3)
	crime_ann.addModule(hiddenLayer4)
	crime_ann.addModule(hiddenLayer5)
	crime_ann.addOutputModule(outLayer)
	in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
	hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
	hidden2_to_hidden3 = FullConnection(hiddenLayer2, hiddenLayer3)
	hidden3_to_hidden4 = FullConnection(hiddenLayer3, hiddenLayer4)
	hidden4_to_hidden5 = FullConnection(hiddenLayer4, hiddenLayer5)
	hidden5_to_out = FullConnection(hiddenLayer5, outLayer)
	crime_ann.addConnection(in_to_hidden1)
	crime_ann.addConnection(hidden1_to_hidden2)
	crime_ann.addConnection(hidden2_to_hidden3)
	crime_ann.addConnection(hidden3_to_hidden4)
	crime_ann.addConnection(hidden4_to_hidden5)
	crime_ann.addConnection(hidden5_to_out)
	crime_ann.sortModules()


	trainer = BackpropTrainer( crime_ann,dataset )

	print "-------------------------------------------------"


	rmse_vector = []
	print "training for {} epochs...".format( epochs )
	for i in range( epochs ):
		mse = trainer.train()
		rmse = sqrt( mse )
		print "training RMSE, epoch {}: {}".format( i + 1, rmse )
		rmse_vector.append(rmse)

	print "-------------------------------------------------"
	
	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

	print "Training done!"
	print "-------------------------------------------------"

	return rmse_vector


def train_2_hidden():

	print "-------------------------------------------------"
	print "loading data..."
	print "file to be loaded: ", train_file

	# regresa un ndarray de numpy
	train = np.loadtxt( train_file, delimiter = ',' )

	print "data loaded to a ", type(train),   " of size: ", train.shape, " and type:", train.dtype
	print "Spliting inputs and output for training..."

	inputs_train = train[:,0:-1]
	output_train = train[:,-1]
	output_train = output_train.reshape( -1, 1 )


	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(output_train),   " of size: ", output_train.shape, " and type:", output_train.dtype
	print "-------------------------------------------------"



	print "Setting up supervised dataset por pyBrain training..."
	input_size = inputs_train.shape[1]
	target_size = output_train.shape[1]
	dataset = SDS( input_size, target_size )
	dataset.setField( 'input', inputs_train )
	dataset.setField( 'target', output_train )
	print "-------------------------------------------------"



	print "Setting up network for supervised learning in pyBrain..."
	#crime_network = buildNetwork( input_size, hidden_size, target_size, bias = True, hiddenclass = SigmoidLayer, outclass = LinearLayer )
	
	


	crime_ann = FeedForwardNetwork()

	inLayer = LinearLayer(input_size)
	#hiddenLayer1 = TanhLayer(hidden_size)
	#hiddenLayer2 = TanhLayer(hidden_size)
	hiddenLayer1 = SigmoidLayer(hidden_size)
	hiddenLayer2 = SigmoidLayer(hidden_size)
	
	outLayer = LinearLayer(target_size)
	crime_ann.addInputModule(inLayer)
	crime_ann.addModule(hiddenLayer1)
	crime_ann.addModule(hiddenLayer2)
	
	crime_ann.addOutputModule(outLayer)
	in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
	hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
	hidden2_to_out = FullConnection(hiddenLayer2, outLayer)
	crime_ann.addConnection(in_to_hidden1)
	crime_ann.addConnection(hidden1_to_hidden2)
	crime_ann.addConnection(hidden2_to_out)
	crime_ann.sortModules()


	trainer = BackpropTrainer( crime_ann,dataset )

	print "-------------------------------------------------"


	rmse_vector = []
	print "training for {} epochs...".format( epochs )
	for i in range( epochs ):
		mse = trainer.train()
		rmse = sqrt( mse )
		print "training RMSE, epoch {}: {}".format( i + 1, rmse )
		rmse_vector.append(rmse)

	print "-------------------------------------------------"
	
	pickle.dump( crime_ann, open( output_model_file, 'wb' ))

	print "Training done!"
	print "-------------------------------------------------"

	return rmse_vector






def activate_network(test_file):
	colors = cycle(["b", "g", "r", "c", "y", "k"])
	regression_list = []
	factual_data_list = []
	# regresa un ndarray de numpy
	data = np.loadtxt( test_file, delimiter = ',' )

	print "data loaded to a ", type(data),   " of size: ", data.shape, " and type:", data.dtype
	print "Spliting inputs and output for training..."

	inputs_train = data[:,0:-1]
	output_train = data[:,-1]
	output_train = output_train.reshape( -1, 1 )


	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(output_train),   " of size: ", output_train.shape, " and type:", output_train.dtype
	print "-------------------------------------------------"

	min_error = 0.0
	max_error = 0.0
	average_error = 0.0

	print "loading trained model from file..."
	net = pickle.load( open( output_model_file, 'rb' ))
	for i in range(inputs_train.shape[0]):
		regression = net.activate(inputs_train[i])
		current_error = abs(regression-output_train[i])*100
		print "inputs.. ", inputs_train[i][0:3],  "   regression aproximation: ", regression,   " --> real output: ", output_train[i],   " --> error %: ", current_error
		if min_error > current_error:
			min_error = current_error
		if max_error < current_error:
			max_error = current_error
		average_error += current_error
		regression_list.append(regression)
		factual_data_list.append(output_train[i])

	average_error /= inputs_train.shape[0]

	print "Maximum error: ", max_error
	print "Minimum error: ", min_error
	print "Average error: ", average_error


	labels = [i for i in range(inputs_train.shape[0])]
	fig, ax = plt.subplots()
	index = np.arange(inputs_train.shape[0])
	bar_width = 0.35
	rects1 = plt.bar(index, regression_list, bar_width, label="Prediccion", color=colors.next())
	rects2 = plt.bar(index + bar_width, factual_data_list, bar_width, label="Referencia", color=colors.next())
	plt.xticks(index + bar_width, labels)
	plt.tight_layout()
	plt.legend()
	plt.show()








#train_2_hidden()
#activate_network(test_file)




