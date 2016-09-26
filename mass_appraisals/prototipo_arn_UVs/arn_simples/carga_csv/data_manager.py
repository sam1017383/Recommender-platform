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

import csv
import re

import visualizer

def load_csv(csv_file):
	'load csv file to list of dictionaries'
	try:
		data = []
		raw_data = csv.DictReader(open(csv_file))
		#print "Data loaded!", raw_data
		for each_row in raw_data:
			data.append(each_row)
		return data
	except ValueError:
		print "Error: " + str(ValueError)	
		return []





























		

file_name = "quintanaroo_abril_2015"
data_dict_avaluos = load_csv(file_name+'.csv')

for i in data_dict_avaluos[:2]:
	print i.keys()


print visualizer.dot_infomap_from_appraisals(data_dict_avaluos, "UVs_map_"+file_name)


