import numpy as np
from abc import ABC, abstractmethod
from math import exp, log


from .LossTypes import LossTypes
from ...DerivableFunction import DerivableFunction

EPSILON = 10E-8

class Loss(DerivableFunction):

	"""
	Every Loss function must be derived from this class.

	__call__(X, Y): X is the predicted output, Y the actual label.
	"""

	def __init__(self, function):

		super().__init__(function)
		self.lossType = None

	@abstractmethod
	def __call__(self, X: np.array, Y: np.array):
		#X is the prediction and Y the label
		pass

	@abstractmethod
	def __str__(self):
		pass

class L1_Loss(Loss):

	def L1(X: np.array, Y: np.array):

		return np.sum(np.sum(np.absolute((Y-X)), axis=1), axis=0) / (X.shape[0]*X.shape[1])

	def L1_d(X: np.array, Y: np.array):

		shape = X.shape
		back = np.zeros(X.shape)
		for i in range(shape[0]):
			for j in range(shape[1]):

				x, y = X[i, j], Y[i, j]
				if (x > y):
					back[i, j] = 1
				elif (x == y):
					back[i, j] = 0
				else:
					back[i, j] = -1
					
		back /= X.shape[1]
		return back

	def __init__(self):

		super().__init__(L1_Loss.L1)

		self.lossType = LossTypes.L1_LOSS

	def derivative(self):

		if (self._order == 0):

			back = L1_Loss()
			back.set_function(L1_Loss.L1_d)
			back._order += 1

			return back
		else:
			return None

	def __call__(self, X: np.array, Y: np.array):

		return self._function(X, Y)

	def __str__(self):

		return "L1 Loss"  + "'"*self._order



class L2_Loss(Loss):
	
	def L2(X: np.array, Y: np.array):

		return np.sum(np.sum(0.5*(Y-X)**2, axis=1), axis=0) / (X.shape[0]*X.shape[1])

	def L2_d(X: np.array, Y: np.array):

		shape = X.shape
		back = np.zeros(X.shape)
		for i in range(shape[0]):
			for j in range(shape[1]):

				x, y = X[i, j], Y[i, j]
				
				back[i, j] = (x-y) / X.shape[1]

		return back

	def __init__(self):

		super().__init__(L2_Loss.L2)

		self.lossType = LossTypes.L2_LOSS

	def derivative(self):

		if (self._order == 0):

			back = L2_Loss()
			back.set_function(L2_Loss.L2_d)
			back._order += 1

			return back
		else:
			return None

	def __call__(self, X: np.array, Y: np.array):

		return self._function(X, Y)

	def __str__(self):

		return "L2 Loss" + "'"*self._order

class Binary_Cross_Entropy_Loss(Loss):


	def BCEL(X: np.array, Y: np.array):

		#handling intern conversion
		CEMatrix = -(Y * np.log(X+EPSILON) + (1-Y)*np.log(1-X+EPSILON))

		return np.sum(np.sum(CEMatrix, axis=1), axis=0) / (X.shape[0]*X.shape[1])

	def BCEL_d(X: np.array, Y: np.array):

		shape = X.shape
		back = np.zeros(X.shape)
		for i in range(shape[0]):
			for j in range(shape[1]):

				x, y = X[i, j], Y[i, j]
				
				back[i, j] = -(y/(x+EPSILON) - (1-y)/(1-x+EPSILON))

		back /= X.shape[1]

		return back

	def __init__(self):

		super().__init__(Binary_Cross_Entropy_Loss.BCEL)

		self.lossType = LossTypes.BINARY_CROSS_ENTROPY_LOSS

	def derivative(self):

		if (self._order == 0):

			back = Binary_Cross_Entropy_Loss()
			back.set_function(Binary_Cross_Entropy_Loss.BCEL_d)
			back._order += 1

			return back
		else:
			return None

	def __call__(self, X: np.array, Y: np.array):

		return self._function(X, Y)

	def __str__(self):

		return "Binary_Cross_Entropy_Loss" + "'"*self._order
	


class Categorical_Cross_Entropy_Loss(Loss):
	
	def CCEL(X: np.array, Y: np.array):

		CEMatrix = -(Y * np.log(np.maximum(X, EPSILON)))

		return np.sum(CEMatrix) / (X.shape[0])

	def CCEL_d(X: np.array, Y: np.array):

		 # Number of samples
	    m = X.shape[1]
	    
	    # Calculate the derivative
	    return -(Y/(X + EPSILON))/m

	def __init__(self):

		super().__init__(Categorical_Cross_Entropy_Loss.CCEL)

		self.lossType = LossTypes.CATEGORICAL_CROSS_ENTROPY_LOSS

	def derivative(self):

		if (self._order == 0):

			back = Categorical_Cross_Entropy_Loss()
			back.set_function(Categorical_Cross_Entropy_Loss.CCEL_d)
			back._order += 1

			return back
		else:
			return None

	def __call__(self, X: np.array, Y: np.array):

		return self._function(X, Y)

	def __str__(self):

		return "Categorical_Cross_Entropy_Loss" + "'"*self._order

class Softmax_Categorical_Cross_Entropy_Loss(Categorical_Cross_Entropy_Loss):

	def CCEL_d(X: np.array, Y: np.array):

		 # Number of samples
	    m = X.shape[1]
	    
	    # Calculate the derivative
	    return (X-Y)/m

	def __init__(self):

		super().__init__()

		self.lossType = LossTypes.SOFTMAX_CROSS_ENTROPY_LOSS

	def derivative(self):

		if (self._order == 0):

			back = Softmax_Categorical_Cross_Entropy_Loss()
			back.set_function(Softmax_Categorical_Cross_Entropy_Loss.CCEL_d)
			back._order += 1

			return back
		else:
			return None

class PerceptronCriterion(Loss):

	"""
	Assume that the output is of type -1, 1
	"""

	def loss(X: np.array, Y: np.array):

		return np.sum(X != Y)

	def loss_d(X: np.array, Y: np.array):

		height, width = X.shape[0], X.shape[1]

		back = np.zeros(X.shape)

		for i in range(height):
			for j in range(width):

				back[i, j] = max(0, -Y[i, j]*X[i, j])

		return back


	def __init__(self):

		super().__init__(PerceptronCriterion.loss)

	def __call__(self, X: np.array, Y: np.array):
		
		return self._function(X, Y)

	def __str__(self):

		return "PerceptronCriterion" + "'"*self._order

	def derivative(self):

		if (self._order == 0):

			back = PerceptronCriterion()
			back.set_function(PerceptronCriterion.loss_d)
			back._order += 1
			return back

		else:

			return None

class HingeLoss(Loss):

	"""
	Assume that the output is of type -1, 1
	"""

	def loss(X: np.array, Y: np.array):

		return np.sum(X != Y)

	def loss_d(X: np.array, Y: np.array):

		height, width = X.shape[0], X.shape[1]

		back = np.zeros(X.shape)

		for i in range(height):
			for j in range(width):

				back[i, j] = max(0, 1-Y[i, j]*X[i, j])

		return back


	def __init__(self):

		super().__init__(HingeLoss.loss)

	def __call__(self, X: np.array, Y: np.array):
		
		return self._function(X, Y)

	def __str__(self):

		return "HingeLoss" + "'"*self._order

	def derivative(self):

		if (self._order == 0):

			back = HingeLoss()
			back.set_function(HingeLoss.loss_d)
			back._order += 1
			return back

		else:

			return None



class  WestonWatkinsLoss(Loss):

	def loss(X: np.array, Y: np.array):

		X = X.T
		Y = Y.T

		total_sum: float = 0

		height, width = X.shape

		for i in range(height):

			x = X[i]
			y = Y[i]

			#finding the class separator, one hot encoding is assumed
			C = np.argmax(y)
			#prediction value for class
			xc = x[C] 
			#creating a list of values:
			for j in range(width):
				if j != C:
					margin = x[j] - xc + 1
					total_sum += max(0, margin)

		return total_sum



	def loss_d(X: np.array, Y: np.array):


		width, height = X.shape

		#error container
		Error = np.zeros(X.shape)

		for i in range(height):

			x = X[:, i:i+1]
			y = Y[:, i:i+1]

			#calculating class identifier, assuming one hot encoding 
			c = np.argmax(y.T)
			#now counting what contributed positively
			contribs = [(1 if ((x[j, 0]-y[c, 0] + 1) > 0)  else 0) for j in range(width)]

			#inserting 1 if positively contributed and not class, else sum of all false contributions
			for j in range(width):

				if j != c:

					Error[j, i] = contribs[j]

				else:

					Error[j, i] = -(sum([el for el in contribs]) - contribs[c])

		return Error


	def __init__(self):

		super().__init__(WestonWatkinsLoss.loss)


	def __call__(self, X: np.array, Y: np.array):

		return self._function(X, Y)

	def __str__(self):

		return "WestonWatkinsLoss" + "'"*self._order

	def derivative(self):

		if (self._order == 0):

			back = WestonWatkinsLoss()
			back.set_function(WestonWatkinsLoss.loss_d)
			back._order += 1
			return back

		else:

			return None


#final map
LossMap: dict = 	{
						LossTypes.L1_LOSS : L1_Loss,
						LossTypes.L2_LOSS : L2_Loss,
						LossTypes.CATEGORICAL_CROSS_ENTROPY_LOSS : Categorical_Cross_Entropy_Loss,
						LossTypes.BINARY_CROSS_ENTROPY_LOSS : Binary_Cross_Entropy_Loss,		
						LossTypes.SOFTMAX_CROSS_ENTROPY_LOSS : Softmax_Categorical_Cross_Entropy_Loss,
						#following ones are only for internal use
						LossTypes.PERCEPTRON_CRITERION : PerceptronCriterion,
						LossTypes.HINGE_LOSS : HingeLoss,
						LossTypes.WESTON_WATKINS_LOSS : WestonWatkinsLoss,
					}