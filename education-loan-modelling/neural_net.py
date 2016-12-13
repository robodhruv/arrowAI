from numpy import exp, array, random, dot, sum, size, absolute, asfarray
import numpy as np
from csv import reader
import pickle, joblib
import sys
import math
import random

random.seed(0)
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset


def normalise(data):
	data = array(data)
	mean = np.mean(data, axis=0)
	data -= mean
	std = np.std (data, axis = 0)
	data /= std
	return data, mean, std

# calculate a random number where:  a <= rand < b
def rand(a, b):
	return (b-a)*random.random() + a

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
	return np.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
	return 1.0 - y**2


class DB:
	def __init__(self):
		self.institutes = {}

	def create_brain(self, institute, ni, nh, no):
		brain = NN(ni, nh, no, True)
		self.institutes.update({institute: brain})

		return brain


class NN:
	def __init__(self, ni, nh, no, regression = False):
		"""
		The NN constructor.
		
		ni, nh, no are the number of input, hidden and output nodes.
		regression is used to determine if the Neural network will be trained 
		and used as a classifier or for function regression.

		"""
		
		self.regression = regression
		
		#Number of input, hidden and output nodes.
		self.ni = int(ni  + 1) # +1 for bias node
		self.nh = int(nh  + 1) # +1 for bias node
		self.no = int(no)

		# activations for nodes
		# NumPy avoided as np.ones([1, self.ni]) takes 4 times longer!
		self.ai = [1.0]*self.ni
		self.ah = [1.0]*self.nh
		self.ao = [1.0]*self.no
		
		# create weights and set to random values
		self.wi = np.random.rand(self.ni, self.nh)
		self.wo = np.random.rand(self.nh, self.no)
		

		# last change in weights for momentum   
		self.ci = np.zeros([self.ni, self.nh])
		self.co = np.zeros([self.nh, self.no])

		self.input_mean = [0.0]*int(ni)
		self.input_std = [0.0]*int(ni)

		self.output_mean = [0.0]*int(no)
		self.output_std = [0.0]*int(no)

	def normalise_input(self, input):
		normalised = (asfarray(input) - asfarray(self.input_mean))
		normalised /= asfarray(self.input_std)
		normalised = list(normalised)
		return normalised

	def real_output(self, output):
		real = (asfarray(output) * asfarray(self.output_std)) + asfarray(self.output_mean)
		return real

	def update(self, inputs):
		if len(inputs) != self.ni-1:
			raise ValueError, 'wrong number of inputs'

		# input activations
		# self.ai = list(inputs)
		# self.ai.append(1)
		# The above seems faster, but benchmarking yields that the below
		# primitive method for assignment is faster.
		for i in range(self.ni - 1):
			self.ai[i] = inputs[i]
		
		self.ah = sigmoid(np.dot(asfarray(self.wi).T, asfarray(self.ai)))

		# Calculating Outputs

		self.ao = np.dot(asfarray(self.wo).T, asfarray(self.ah))
		if not self.regression:
			self.ao = sigmoid(self.ao)
		
		return self.ao[:]



	def backPropagate(self, targets, N, M):
		if len(targets) != self.no:
			raise ValueError, 'wrong number of target values'

		# calculate error terms for output
		output_deltas = asfarray(targets) - self.ao
		if not self.regression:
			output_deltas = dsigmoid(self.ao)*output_deltas

		# calculate error terms for hidden

		hidden_deltas = dsigmoid(self.ah) * np.dot(self.wo, output_deltas)

		# update output weights
		# Not vectorising, because of momentum effects!
		# M eases convergence
		for j in range(self.nh):
			for k in range(self.no):
				change = output_deltas[k]*self.ah[j]
				self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
				self.co[j][k] = change

		# update input weights
		for i in range(self.ni):
			for j in range(self.nh):
				change = hidden_deltas[j]*self.ai[i]
				self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
				self.ci[i][j] = change


		# Calculate and return error
		error = 0.5*((asfarray(targets) - self.ao)**2)
		return error

		
	def weights(self):
		print 'Input weights:'
		print self.wi

		print
		print 'Output weights:'
		print self.wo

	def load_norms(self, norms):

		self.input_mean = norms[0]
		self.input_std = norms[1]

		self.output_mean = norms[2]
		self.output_std = norms[3]


	def train(self, patterns, norms, iterations, epsilon, N=0.5, M=0.1, verbose = False):
		"""Train the neural network.  
		
		N is the learning rate.
		M is the momentum factor.
		"""
		self.load_norms(norms)

		error = 10
		error_prev = 0
		for i in xrange(iterations):
			if (abs(error - error_prev) > epsilon) or error_prev > epsilon*100 :
				error_prev = error
				error = 0.0
				for p in patterns:
					self.update(p[0])
					tmp = self.backPropagate(p[1], N, M)
					error += tmp
				
				if i % 100 == 0:
					print str(i/100) + ' error %-14f' % error


			else:
				print "Trained to accuracy " + str(epsilon)
				break



if sys.argv[1] == "train":
	student_data = load_csv("student_data.csv")
	college_data = load_csv("institutes.csv")

	# relevant indices according to the zipped 2D list obtained from
	# the two files; order is college_data:student_data
	
	rel_input_sanction = [11, 12, 14] # Input params
	rel_output_sanction = [10] # Output params
	input_institute_name = [1] # Institute Names

	hidden_layers = 4 # change this to change the model

	# Create a unique list of institutes from the dataset
	institutes = list()
	for row in college_data:
		institutes.append(row[1])
	institutes = list(set(institutes))

	database = DB()
	for institute in institutes:
		inputs = []
		for row1 in college_data:
			row_clone = list(row1)
			if (row1[1] == institute):
				for row2 in student_data:
					if row2[0]==row1[0]:
						row_clone.extend(row2[1:])
						break
				inputs.append(row_clone)
		
		inputs = array(inputs)
		sanction_inputs = []
		sanction_outputs = []
		for row in inputs:
			sanction_inputs.append(map(float, list(row[[rel_input_sanction]])))
			sanction_outputs.append(map(float, list(row[[rel_output_sanction]])))
		
		epsilon = 1e-5 # Degree of convergence of the descent
		max_iter = 10000 # Upper bound on the number of iterations
		learning_rate = 0.01
		momentum_rate = 0.1


		sanction_outputs = np.asfarray(sanction_outputs)
		sanction_inputs = np.asfarray(sanction_inputs)

		sanction_inputs, input_mean, input_std = normalise(sanction_inputs)
		sanction_outputs, output_mean, output_std = normalise(sanction_outputs)
		norms = [input_mean, input_std, output_mean, output_std]

		data = []
		for i in range(len(sanction_inputs)):
			data.append([sanction_inputs[i], sanction_outputs[i]])

		brain = database.create_brain(institute, len(rel_input_sanction), hidden_layers, len(rel_output_sanction))

		brain.train (data, norms, max_iter, epsilon, learning_rate, momentum_rate, False)
	
	joblib.dump(database, "trained_net.pkl")

if sys.argv[1] == "predict":
	database = joblib.load("trained_net.pkl")
	
	while(1):
		institute = str(raw_input("Enter institute: "))
		brain = database.institutes[institute]

		input_string = raw_input("Enter Details: ")
		input_data = map(float, input_string.split())
		input_data[2] = math.log(input_data[2])
		normalised_input = brain.normalise_input(input_data)
		print normalised_input

		output = brain.update(normalised_input)

		print brain.real_output(output)
