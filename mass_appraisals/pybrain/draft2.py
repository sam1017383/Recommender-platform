import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import numpy as np
import cPickle as pickle
from math import sqrt
import scipy
import os

from pybrain.datasets.supervised import SupervisedDataSet as SDS
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

output_model_file = 'crime_model_100h_100h_600e.pkl'
train_file = 'crimerate_extract_numeric.csv'

def train():

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
	hidden_size = 100
	epochs = 1000
	#crime_network = buildNetwork( input_size, hidden_size, target_size, bias = True, hiddenclass = SigmoidLayer, outclass = LinearLayer )
	
	


	crime_ann = FeedForwardNetwork()

	inLayer = LinearLayer(input_size)
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





def activate_network():

	# regresa un ndarray de numpy
	data = np.loadtxt( train_file, delimiter = ',' )

	print "data loaded to a ", type(data),   " of size: ", data.shape, " and type:", data.dtype
	print "Spliting inputs and output for training..."

	inputs_train = data[:,0:-1]
	output_train = data[:,-1]
	output_train = output_train.reshape( -1, 1 )


	print "inputs in a ", type(inputs_train),   " of size: ", inputs_train.shape, " and type:", inputs_train.dtype
	print "output in a ", type(output_train),   " of size: ", output_train.shape, " and type:", output_train.dtype
	print "-------------------------------------------------"



	print "loading trained model from file..."
	net = pickle.load( open( output_model_file, 'rb' ))
	for i in range(10):
		regression = net.activate(inputs_train[i])
		print "inputs.. ", inputs_train[i][0:3],  "   regression aproximation: ", regression,   " --> real output: ", output_train[i],   " --> error %: ", abs(output_train[i]-regression)/output_train[i]*100





train()
activate_network()








