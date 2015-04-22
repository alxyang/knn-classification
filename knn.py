import re
import numpy
import math
import random

training_set = []
validation_set = []
test_set = []



def load(fn, ds):
	f = open(fn, "r")
	for line in f:
		tokens = line.split()
		features = []
		for i in range(0, len(tokens) - 1):
			features.append(float(tokens[i]))
		data = (features, int(tokens[len(tokens) - 1]))
		ds.append(data)

def distance(feature1, feature2):
	distance = float(0)
	for i in range(0, len(feature1)):
		distance  = distance + math.pow(feature1[i] - feature2[i],2)
	distance = math.sqrt(distance)
	return distance


def check_data(test_point, data_point, ds, k):
	d = distance(test_point[0], data_point[0])
	if len(ds) < k:
		ds.append((d,test_point[1]))
	else:
		index = 0
		maxDist = float(ds[0][0])
		for i in range(1, len(ds)):
			(dist, label) = ds[i]
			if (dist > maxDist):
				maxDist = dist
				index = i
		if (d < maxDist):
			ds[index] = (d, test_point[1])

def calc_error(k, tr_set, v_set):
	num_samples = len(v_set)
	errors = 0

	debug_counter  = 0

	for (v_feature, v_label) in v_set:
		ds = []
		for training_point in tr_set:
			check_data(training_point, (v_feature, v_label), ds, k)

		counter = [0,0,0,0,0,0,0,0,0,0]
		for (dist, lab) in ds:
			counter[lab] = counter[lab] + 1
		
		m_counter = -1
		predict = -1

		for i in range(0, len(counter)):
			if counter[i] > m_counter:
				m_counter = counter[i]
				predict = i

		random_labels = []
		for i in range(0, len(counter)):
			if counter[i] == m_counter:
				random_labels.append(i)

		predict = random_labels[random.randrange(0,len(random_labels))]
		if not(predict == v_label):
			errors = errors + 1

		debug_counter = debug_counter  + 1
	return float(errors)/num_samples

def calculate_confusion_matrix(k, tr_set, v_set):
	counter_label = [0,0,0,0,0,0,0,0,0,0]
	confusion_matrix = []
	for i in range(0,10):
		confusion_matrix.append([float(0),float(0),float(0),float(0),float(0),float(0),float(0),float(0),float(0),float(0)])
	
	for (v_feature, v_label) in v_set:
		ds = []
		for training_point in tr_set:
			check_data(training_point, (v_feature, v_label), ds, k)

		counter = [0,0,0,0,0,0,0,0,0,0]
		for (dist, lab) in ds:
			counter[lab] = counter[lab] + 1

		m_counter = -1
		predict = -1

		for i in range(0, len(counter)):
			if counter[i] > m_counter:
				m_counter = counter[i]
				predict = i

		random_labels = []
		for i in range(0, len(counter)):
			if counter[i] == m_counter:
				random_labels.append(i)

		predict = random_labels[random.randrange(0,len(random_labels))]
		confusion_matrix[predict][v_label] = confusion_matrix[predict][v_label] + 1
		counter_label[v_label] = counter_label[v_label] + 1


	for i in range(0, len(confusion_matrix)):
		for j in range(0, len(confusion_matrix[i])):
			confusion_matrix[i][j] = confusion_matrix[i][j] / counter_label[j] 
	print_confusion_matrix(confusion_matrix)

def print_confusion_matrix(matrix):	
	for row in matrix:
		print row
		

load("hw2train.txt", training_set)
load("hw2validate.txt", validation_set)
load("hw2test.txt", test_set)

calculate_confusion_matrix(3, training_set, test_set)
	


