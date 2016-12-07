from numpy import exp, array, random, dot, sum, size, absolute
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
    data -= np.mean(data, axis=0)
    data /= np.std (data, axis = 0)
    return data

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2


def plot(inputs, outputs, actual):
    """Plot a given function.  
    
    The actual function will be plotted with a line and the outputs with 
    points.  Useful for visualizing the error of the neural networks attempt 
    at function interpolation."""
    try:
        import matplotlib.pyplot
    except:
        raise ImportError, "matplotlib package not found."
    fig = matplotlib.pyplot.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(inputs, actual, 'b-')
    ax1.plot(inputs, outputs, 'r.')
    matplotlib.pyplot.draw()
    
    

class NN:
    def __init__(self, ni, nh, no, regression = False):
        """NN constructor.
        
        ni, nh, no are the number of input, hidden and output nodes.
        regression is used to determine if the Neural network will be trained 
        and used as a classifier or for function regression.
        """
        
        self.regression = regression
        
        #Number of input, hidden and output nodes.
        self.ni = ni  + 1 # +1 for bias node
        self.nh = nh  + 1 # +1 for bias node
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-1, 1)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-1, 1)

        # last change in weights for momentum   
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)


    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh - 1):
            total = 0.0
            for i in range(self.ni):
                total += self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(total)

        # output activations
        for k in range(self.no):
            total = 0.0
            for j in range(self.nh):
                total += self.ah[j] * self.wo[j][k]
            self.ao[k] = total
            if not self.regression:
                self.ao[k] = sigmoid(total)
            
        
        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            output_deltas[k] = targets[k] - self.ao[k]
            if not self.regression:
                output_deltas[k] = dsigmoid(self.ao[k]) * output_deltas[k]

        
        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
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

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error += 0.5*((targets[k]-self.ao[k])**2)
        return error


    def test(self, patterns, verbose = False):
        tmp = []
        for p in patterns:
            if verbose:
                print p[0], '->', self.update(p[0])
            tmp.append(self.update(p[0]))

        return tmp

        
    def weights(self):
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]
        print
        print 'Output weights:'
        for j in range(self.nh):
            print self.wo[j]

    def train(self, patterns, iterations=1000, N=0.5, M=0.1, verbose = False):
        """Train the neural network.  
        
        N is the learning rate.
        M is the momentum factor.
        """
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                self.update(p[0])
                tmp = self.backPropagate(p[1], N, M)
                error += tmp
                
            if i % 100 == 0:
                print 'error %-14f' % error


if sys.argv[1] == "train":
    student_data = load_csv("student_data.csv")
    college_data = load_csv("institutes.csv")

    rel_input_sanction = [14, 15, 13]
    rel_output_sanction = [10]

    institutes = ["A"]
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
    		sanction_inputs.append(map(int, list(row[[rel_input_sanction]])))
    		sanction_outputs.append(map(int, list(row[[rel_output_sanction]])))
    	
    	epsilon = 1e-5
    	max_iter = 10000
        learning_rate = 0.25

    	sanction_outputs = np.asfarray(sanction_outputs)
    	sanction_inputs = np.asfarray(sanction_inputs)


        sanction_inputs = normalise(sanction_inputs)
        sanction_outputs = normalise(sanction_outputs)

        data = []
        for i in range(len(sanction_inputs)):
            data.append([sanction_inputs[i], sanction_outputs[i]])


        brain = NN (3, 4, 1, regression = True)
        brain.train (data, 50000, 0.01, 0.1, False)
        joblib.dump(brain, "trained_net.pkl")
if sys.argv[1] == "predict":
    brain = joblib.load("trained_net.pkl")
    
    while(1):
        input_string = raw_input("Enter Details:")
        details = map(int, input_string.split())

        output = brain.update(details)
        print output