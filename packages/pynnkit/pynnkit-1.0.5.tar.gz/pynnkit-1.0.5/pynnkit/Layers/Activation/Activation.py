"""
Activation class represents a DerivableFunction
"""
import numpy as np
from abc import ABC, abstractmethod
from math import exp

from ...DerivableFunction import DerivableFunction
from .ActivationTypes import ActivationTypes

EPSILON = 10E-8
MAX_EXPONENT = 1E2

class Activation(DerivableFunction):

	"""
	Base class for all activations.
	Derived classes must implement:

	__call__(X_in, X_out), where X_in is the input to this function,
						   and output is what the function produced.
	"""

	def __init__(self, function):

		super().__init__(function)
		self.activationType = None

	@abstractmethod
	def __call__(self, X_in: np.array, X_out: np.array):
		#X_in and X_out are column vectors
		pass

class Sigmoid(Activation):

	def sigmoid(x):

		if (x > 0):
			x = min(x, MAX_EXPONENT)
		else:
			x = max(x, -MAX_EXPONENT)

		return (1)/(1+exp(-x))

	def sigmoid_d(X_out):

		#gets the output as a column vector
		D = X_out.shape[0]
		back = np.eye(D)
		for i in range(D):
			back[i, i] = X_out[i] * (1-X_out[i])

		return back


	def __init__(self):


		sigmoid = np.vectorize(Sigmoid.sigmoid)

		super().__init__(sigmoid)

		self.activationType = ActivationTypes.SIGMOID

	def derivative(self):

		if (self._order == 0):

			back = Sigmoid()
			back.set_function(Sigmoid.sigmoid_d)
			back._order += 1 #increasing order to 1
			
			return back
	
		else:
			return None #no further derivative needed

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if (self._function is None):
			return None

		#depending on what order this function is, it uses a different matrix
		if (self._order == 0):
			return self._function(X_in)
		elif (self._order == 1):
			return self._function(X_out)


	def __str__(self):
		return "Sigmoid" + "'"*self._order

class ReLU(Activation):

	def relu(x):

		return (0 if x < 0 else x)

	def relu_d(X_in):

		#gets the input as a column vector
		D = X_in.shape[0]
		back = np.eye(D)
		for i in range(D):
			back[i, i] = (1 if X_in[i] > 0 else 0)

		return back

	def __init__(self):

		super().__init__(np.vectorize(ReLU.relu))

		self.activationType = ActivationTypes.RELU

	def derivative(self):

		if (self._order == 0):

			back = ReLU()
			back.set_function(ReLU.relu_d)
			back._order += 1

			return back

		else:
			return None

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if(self._function is None):
			return None

		return self._function(X_in)

	def __str__(self):

		return "ReLU" + "'"*self._order

class Sign(Activation):

	def sign(x):

		return (-1 if x < 0 else 1)

	def sign_d(X_in):

		D = X_in.shape[0]
		return np.eye(D)

	def __init__(self):

		sign = np.vectorize(Sign.sign)
		super().__init__(sign)
		self.activationType = ActivationTypes.SIGN

	def derivative(self):

		if (self._order == 0):

			back = Sign()
			#cheap trick: return the input
			back.set_function(Sign.sign_d)
			back._order += 1

			return back

		else:
			return None

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if(self._function is None):
			return None

		return self._function(X_in)

	def __str__(self):

		return "Sign"  + "'"*self._order

class Tanh(Activation):

	def tanh(x: float):

		if (x > 0):
			x = min(x, MAX_EXPONENT)
		else:
			x = max(x, -MAX_EXPONENT)

		ep = exp(x)
		em = exp(-x)

		return ((ep-em)/(ep+em + EPSILON))

	def tanh_d(X_out):

		D = X_out.shape[0]
		back = np.eye(D)
		for i in range(D):
			back[i] = (1-X_out[i]*X_out[i])
		return back

	def __init__(self):

		super().__init__(np.vectorize(Tanh.tanh))
		self.activationType = ActivationTypes.TANH

	def derivative(self):

		if (self._order == 0):

			back = Tanh()
			back.set_function(Tanh.tanh_d)
			back._order += 1

			return back

		else:
			return None

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if(self._function is None):
			return None

		if (self._order == 0):

			return self._function(X_in)

		elif (self._order == 1):

			return self._function(X_out)


	def __str__(self):

		return "Tanh" + "'"*self._order

class Linear(Activation):

	def linear(X):
		return X

	def linear_d(X_in):

		D = X_in.shape[0]
		return np.eye(D)

	def __init__(self):

		super().__init__(Linear.linear)
		self.activationType = ActivationTypes.LINEAR

	def derivative(self):

		if (self._order == 0):

			back = Linear()
			back.set_function(Linear.linear_d)
			back._order += 1

			return back

		else:
			return None

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if(self._function is None):
			return None

		if (self._order == 0):

			return X_in

		elif (self._order == 1):

			return self._function(X_in)


	def __str__(self):

		return "Linear"  + "'"*self._order

class Softmax(Activation):

	def softmax(X):

		X_exp = np.exp(X)
		npsum = np.sum(X_exp)
		return X_exp / npsum


	def softmax_d(X_out):

		D = X_out.shape[0]

		back = np.zeros((D, D))

		for i in range(D):
			for j in range(D):

				if i == j:

					back[i, j] = X_out[i]*(1-X_out[i])

				else:

					back[i, j] = -X_out[i]*X_out[j]
					
		return back

	def __init__(self):

		super().__init__(Softmax.softmax)
		self.activationType = ActivationTypes.SOFTMAX

	def derivative(self):

		if (self._order == 0):

			back = Softmax()
			back.set_function(Softmax.softmax_d)
			back._order += 1

			return back

		else:
			return None

	def __call__(self, X_in: np.array, X_out: np.array=None):

		if(self._function is None):
			return None

		if self._order == 0:
			return self._function(X_in)
		elif self._order == 1:
			return self._function(X_out) 


	def __str__(self):

		return "Softmax" + "'"*self._order


#final map
ActivationMap: dict = 	{
						ActivationTypes.SIGMOID : Sigmoid,
						ActivationTypes.RELU: ReLU,
						ActivationTypes.SIGN: Sign,
						ActivationTypes.SOFTMAX: Softmax,
						ActivationTypes.LINEAR: Linear,
						ActivationTypes.TANH: Tanh, 
					}